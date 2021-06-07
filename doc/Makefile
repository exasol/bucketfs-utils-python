# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXAPIDOC        ?= sphinx-apidoc 
SOURCEDIR     = .
BUILDDIR      = _build
MODULES_PATH  = ../exasol_bucketfs_utils_python
APIDOC_OUTPUT  = api

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

api-doc:
	@$(SPHINXAPIDOC) -T -d 1 --separate -o "$(APIDOC_OUTPUT)" "$(MODULES_PATH)"

clean-build:
	[ ! -e "$(BUILDDIR)" ] || rm -r "$(BUILDDIR)"
	[ ! -e "$(APIDOC_OUTPUT)" ] || rm -r "$(APIDOC_OUTPUT)"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile api-doc
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
