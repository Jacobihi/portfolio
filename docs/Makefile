# You can set these variables from the command line.
SPHINXOPTS    = -c .
SPHINXBUILD   = sphinx-build
SOURCEDIR     = ../
BUILDDIR      = ./


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


html: 
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -r "$(BUILDDIR)"/*.html "$(BUILDDIR)"/*.inv "$(BUILDDIR)"/*.js  "$(BUILDDIR)"/.doctrees "$(BUILDDIR)"/.doctrees \
	"$(BUILDDIR)"/_sources "$(BUILDDIR)"/_static && rm "$(BUILDDIR)"/.buildinfo


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

