| Test # | When                          | Description                                       | Pass? |
|--------|-------------------------------|---------------------------------------------------|-------|
| 1      | Before pushing to Dev         | Pull from Dev before pushing to Dev               |       |
| 2      | Before pushing to Dev         | Run unitTest.py and pass all tests                |       |
| 3      | Before & After Pushing to Dev | Run protractor tests for middleware functionality |       |
| 4      | After pushing to Dev          | Test that local music runs on page                |       |
| 5      | After pushing to Dev          | Test that local ads run on page                   |       |
| 6      | After pushing to Dev          | Run protractor tests                              |       |
| 7      | After pushing to Dev          | Check that SoundManager is on through browser log |       |
| 8      | Once pushed to Radio1190      | Test that music from their database plays         |       |