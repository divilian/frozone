
## To review ChatLogs
Option 1 (if you have access to the HF project):
1. Clone the repo at this page: https://huggingface.co/datasets/ProjectFrozone/MongoDBDumps
2. Make sure your Mongo server daemon is running. You can tell whether it is via `sudo systemctl status mongod`. If it's down, you can start it via `sudo systemctl start mongod`.
3. Use a `mongorestore` command, with the name of the most recent database dump directory as an argument.  You may also provide `--db` and `--collection` flags to specify where in Mongo the data restores.
4. Open `mongosh`, and `use huggingFaceData` or the name of the DB you restored the data to.
5. To access a specific list of chatlogs: `db.rooms.find({ user_id: { $in: [ list of your chatlog ids ] }})`, or the name of the collection you restored the data to.

Option 2:
1.  Access the Frozone_Data directory that I shared with SD, BH, and GM via OneDrive.  If you are NF, access it via the specific share link that you have.
2.  Change the `USER_IDS` parameter in `data/make_log_files.py` to reflect the user_ids of the chats which you would like to create txt files for.
3.  Run `python -m data.make_log_files`. The appropriate txt files will be created in the `data/experiment_results/Frozone_Data/chatlogs` directory.

## To Run Noah's Scripts
1.  Access the Frozone_Data directory that I shared with SD, BH, and GM via OneDrive.  If you are NF, access it via the specific share link that you have.
2.  Place the entire Frozone_Data directory in the `data/experiment_results/` directory on your local copy of the repo (download it as a .zip and then unzip it in the appropriate location).  MAKE SURE, that `git status` properly ignores all of `Frozone_Data`.
3. Run NF's notebooks in `juypter_notebooks/data_analysis/`.
