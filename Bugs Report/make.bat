@echo off
rem -------------------------------------------------------------------
rem latex -> dvi -> ps -> pdf builder
rem -------------------------------------------------------------------

set name=main

rem -- options --------------------------------------------------------
set options_latex=--src -interaction=nonstopmode
set options_ps=-Ppdf -G0 -ta4
set options_pdf= -dMaxSubsetPct#100 -dCompatibilityLevel#1.4 ^
	-dOptimize#false -dSubsetFonts#true -dEmbedAllFonts#true ^
 	-sPAPERSIZE#a4 -dPDFSETTINGS#/prepress
rem -------------------------------------------------------------------

echo *** START PROCESS ***

rem -- make DVI -------------------------------------------------------
latex %options_latex% %name%.tex
rem -------------------------------------------------------------------

echo *** MAKE BIBLIOGRAPHY ***

rem -- make bibliography ----------------------------------------------
bibtex %name%
rem -------------------------------------------------------------------

echo *** RERUN LATEX ***

rem -- make DVI -------------------------------------------------------
latex %options_latex% %name%.tex
latex %options_latex% %name%.tex
rem -------------------------------------------------------------------

echo *** MAKE POSTSCRIPT FILE ***

rem -- make PS --------------------------------------------------------
dvips %options_ps% -o %name%.ps %name%.dvi
rem -------------------------------------------------------------------

echo *** MAKE PDF ***

rem -- make PDF -------------------------------------------------------
ps2pdf %options_pdf% %name%.ps %name%.pdf
rem -------------------------------------------------------------------

echo *** PRINTING LOG ***

rem -- print warnings, errors, etc. -----------------------------------
findstr.exe /N /I "underfull overfull" "%name%.log"
findstr.exe /N /I "Undefined Missing" "%name%.log"
echo ********** WARNINGS **********
findstr.exe /N /I "Warning" "%name%.log"
echo ********** ERRORS **********
findstr.exe /N /I "error" "%name%.log"
rem -------------------------------------------------------------------

echo *** COMPILATION DONE, Removing temporary files ***

rem -- removing temporary files ---------------------------------------
rm -f *.log *.ps *.dv[ij] *.aux *.toc *.lof *.lot *.[bi]lg *.glo *.gls ^
 	*.idx *.ind *.bbl *.ist *.acn
rem -------------------------------------------------------------------

pause