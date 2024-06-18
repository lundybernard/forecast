clean-notebooks:
	find . -name "*.ipynb" -exec jupyter nbconvert \
	--ClearOutputPreprocessor.enabled=True \
	--ClearMetadataPreprocessor.enabled=True \
	--inplace {} \;

.PHONY: clean-notebooks
