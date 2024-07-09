# Middlebury CS 457: Gender Bias in Machine Translation
## Gender Inference in Spanish to English Translations

### To connect to repo remotely:
1. connect to ada on main level (i.e. username) using Remote Explorer
2. `cd NLP-final-project`
3. *update repository
4. close remote connection

#### Note: before do any below steps, confirm within repository (i.e. NLP-final-project)

### Steps to update repository:
1. `git fetch --all`
2. `git pull` to update to current version of repo
3. *make necessary changes
4. `git add .` to add any new files made
5. `git commit -a -m "[message]"`
6. `git push` to push to repository

The changes should now be in the remote. 

##### Note: if run into problems trying to push "because the remote contains work that you do not have locally":
1. `git fetch --all`
2. `git reset --hard origin/main`

This will be a hard-reset to the most recent commit on the repo.

### Steps to run code to reproduce results:
1. `cd NLP-final-project` (if not already in this main directory)
2. `sbatch main.sbatch`
3. *to watch the job `tail -f [file_name.out]` - the naming convention of the files is `main-[job#].out`
4. *to cancel the job `scancel [job#]`

You can find the final results in `./results/results_[job_scope]_[job#].md`.

##### Note: if need to KeyboardInterrupt, `Cmd` + `c` (on keyboard)
