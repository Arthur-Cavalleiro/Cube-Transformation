@echo off
echo Fixing unrelated histories issue...
git pull --allow-unrelated-histories https://github.com/Arthur-Cavalleiro/Cube-Transformation main

echo.
echo If you encounter merge conflicts, resolve them and then run:
echo git add .
echo git commit -m "Merge remote repository"
echo git push
