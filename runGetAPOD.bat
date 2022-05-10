@echo off
 call C:\ProgramFiles\Anaconda3\Scripts\activate.bat base
"C:\ProgramFiles\Anaconda3\python.exe" "C:\Users\riktonnaer\Documents\Projects\astro_wallpaper_of_the_day\getAPOD.py"
call conda deactivate