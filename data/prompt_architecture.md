# Prompt architecture

### Terminology

FT = "the fine-tuning prompt"; INF = "the inference prompt"

## Labeling suggestion

### System instructions

* **Section `Ia` ("you are a participant")** (lines 1-10) is common to all three
    FT and all three INF prompts.


### Prompt

**Section `Ib` which has in-context learning examples of conversation order

* **Section `II` ("decide whether to respond")** (lines 19-41) should be split
   into `IIcommon`, `IIfro`, `IIcool`, `IIhot`, and should be in both the
   appropriate FT and INF prompts.
* **Section `III` ("decide how to respond")** (lines 42-51) should be split
   into `IIIcommon`, `IIIfro`, `IIIcool`, `IIIhot`, and should be in both the
   appropriate FT and INF prompts.
* I think we're also going to have **Sections `III.FTcommon`, `III.FTfro`,
   `III.FThot`**, and possibly **`III.FTcool`**, which strip things out of the
   `III` prompts that we don't want the fine-tuning process to see.
* **Section `IV` ("your overall goal")** (lines 52-57) should be split into
   `IVcommon`, `IVfro`, `IVcool`, `IVhot`, and should be in both the
   appropriate FT and INF prompts.
* I think we're also going to have **Sections `IV.FTcommon`, `IV.FTfro`,
   `IV.FThot`**, and possibly **`IV.FTcool`**, which strip things out of the
   `IV` prompts that we don't want the fine-tuning process to see.
* **Section `V` ("who you are; transition")** (lines 58-60) is common to all
   three FT and all three INF prompts.

## The prompt components, then, in a nutshell:

1. **I**
1. **II**
1. **IIIcommon** (INF only)
1. **IIIfro** (INF only)
1. **IIIhot** (INF only)
1. **IIIcool** (INF only)
1. **III.FTcommon** (FT only)
1. **III.FTfro** (FT only)
1. **III.FThot** (FT only)
1. **III.FTcool** (FT only)
1. **IVcommon** (INF only)
1. **IVfro** (INF only)
1. **IVhot** (INF only)
1. **IVcool** (INF only)
1. **IV.FTcommon** (FT only)
1. **IV.FTfro** (FT only)
1. **IV.FThot** (FT only)
1. **IV.FTcool** (FT only)
1. **V**

## Wording nitpicks (using `coolbot_prompt_main.txt` line numbers)

1. Lines 25-26 are ambiguous. ("for some time")
2. Line 27 should be reworded ("you may randomly respond") especially in
   conjunction with line 29 ("you should choose not to respond").
3. (Typo on line 36)
4. Line 44 could be made more precise and clear.

## General

1. Add U.S. citizen
