# to run: python -m data.coolbot_training.clean_coolbot_training_no_pass

import re
import pandas as pd

def remove_and_replace_reddit_keywords(df, patterns, replacements):
    # Columns to check
    cols_to_sanitize = ["user_message", "ai_response"]

    # Regex to detect URLs
    url_pattern = re.compile(r"https?://\S+|www\.\S+")

    def mask_urls(text):
        # Function to mask URLs, returning (masked_text, urls)
        # Used to prevent URLs from being removed because of the reddit regexs
        urls = []
        def repl(m):
            urls.append(m.group(0))
            return f"__URL{len(urls)-1}__"  # placeholder
        masked_text = url_pattern.sub(repl, text)
        return masked_text, urls

    def restore_urls(text, urls):
        # Function to restore URLs
        for i, url in enumerate(urls):
            text = text.replace(f"__URL{i}__", url)
        return text

    # Step 1: Drop rows with keywords having no generic replacement
    drop_mask = pd.Series(False, index=df.index)
    for kw, pat in patterns.items():
        if replacements.get(kw) is None:
            cre = re.compile(pat, flags=re.IGNORECASE)
            for col in cols_to_sanitize:
                def check_text(text):
                    masked_text, _ = mask_urls(str(text))
                    return bool(cre.search(masked_text))
                drop_mask |= df[col].apply(check_text)

    df_cleaned = df[~drop_mask].copy()

    # Step 2: Replace keywords with generic equivalents (ignore URLs)
    def replace_keywords_ignore_urls(text):
        text = str(text)
        masked_text, urls = mask_urls(text)
        for kw, pat in patterns.items():
            replacement = replacements.get(kw)
            if replacement is not None:
                masked_text = re.sub(pat, replacement, masked_text, flags=re.IGNORECASE)
        return restore_urls(masked_text, urls)

    for col in cols_to_sanitize:
        df_cleaned[col] = df_cleaned[col].apply(replace_keywords_ignore_urls)
    
    return df_cleaned

if __name__ == "__main__":
    # ingest original data
    df = pd.read_csv("data/coolbot_training/coolBotTrainingNoPass.csv")
    df = df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'])

    # Safe regex patterns relating to reddit giveaways
    patterns = {
        "u/": r"(?<!\w)u/[A-Za-z0-9_-]+",
        "r/": r"(?<!\w)r/[A-Za-z0-9_]+",
        "Reddit": r"\breddits?\b",
        "redditor": r"\bredditors?\b",
        "subreddit": r"\bsubreddits?\b",
        "sub": r"\bsubs?\b",
        "thread": r"\bthread\b",
        "threads": r"\bthreads\b",
        "moderator": r"\bmoderators?\b",
        "automod": r"\bautomods?\b",
        "mod": r"\bmods?\b",
        "upvote": r"\bupvotes?\b",
        "downvote": r"\bdownvotes?\b",
        "karma": r"\bkarma\b",
        "AMA": r"\bAMA\b",
        "AITA": r"\bAITA\b",
        "ELI5": r"\bELI5\b",
        "TIL": r"(?<!\w)(?:TIL|'?til)\b",
        "CMV": r"\bCMV\b",
        "OP": r"(?<!\w)OP(?!\w)",
        "OP's": r"(?<!\w)OP(?:'s)?(?!\w)",
        "OPs": r"(?<!\w)OPs(?!\w)",
        "Edit 2": r"\bEdit\s*2\b",
        "ETA": r"\bETA\b",
        "mods": r"\bmods\b",
        "removed by": r"\bremoved by\b",
        "deleted by": r"\bdeleted by\b",
        ">!": re.escape(">!"),
        "!<": re.escape("!<"),
    }

    # Mapping of keywords to generic equivalents
    # Keywords with no generic analogue are left out or set to None
    replacements = {
        "thread": "conversation",
        "threads": "conversations",
        "TIL": "I learned",
        "OP": "original poster",
        "OP's": "original poster's",
        "OPs": "original posters",
    }

    # Remove and replace 
    df_cleaned = remove_and_replace_reddit_keywords(df, patterns, replacements)
    cols_to_sanitize = ["user_message", "ai_response"]
    df_cleaned = df_cleaned.dropna(subset=cols_to_sanitize).copy()
    print(f"Reddit keywords and nas removed, {100.0 * len(df_cleaned) / len(df):.1f}% of entries retained")
    df_cleaned.reset_index(drop=True, inplace=True)
    df_cleaned.to_csv("data/coolbot_training/coolBotTrainingNoPassCleaned.csv", index=False)
