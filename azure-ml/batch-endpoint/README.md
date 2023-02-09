1. fill in config.json
2. change compute and environment name in pipeline.yml
3. assumption is pipeline_build.py and steps have been constructed already and work - test locally before ci/cd is suggested
4. create github environment such as for dev and put anything with vars.* in the .yml workflows in as variables
5. create secret in environment unless they are repository wide secrets. For example, azure credentials are typically environment specific whereas jfrog login is repository wide
