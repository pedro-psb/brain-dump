.DEFAULT_GOAL := help

LATEXMK ?= latexmk
LATEXINDENT ?= latexindent
TEXCOUNT ?= texcount
UV ?= uv
RSVG_CONVERT ?= rsvg-convert
REFERENCE_SECONDS ?=
SWITCH_COST_SECONDS ?= 5
WATCH ?= 0
BUILD_DIR ?= _build
LATEXMK_FLAGS ?= -pdf -interaction=nonstopmode -synctex=1 -outdir=$(BUILD_DIR)
TEX_FILES := presentation.tex draft.tex

.PHONY: help presentation presentation-build draft draft-build speech-time format clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "%-22s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

$(BUILD_DIR)/pulp-mascot.pdf: assets/pulp-mascot.svg
	@mkdir -p $(BUILD_DIR)
	$(RSVG_CONVERT) --format=pdf --output=$@ $<

$(BUILD_DIR)/pulp-logo.pdf: assets/pulp-logo.svg
	@mkdir -p $(BUILD_DIR)
	$(RSVG_CONVERT) --format=pdf --output=$@ $<

$(BUILD_DIR)/pulp-leaves-cell.pdf: assets/pulp-leaves-cell.svg
	@mkdir -p $(BUILD_DIR)
	$(RSVG_CONVERT) --format=pdf --output=$@ $<

$(BUILD_DIR)/pulp-citrus-cell.pdf: assets/pulp-citrus-cell.svg
	@mkdir -p $(BUILD_DIR)
	$(RSVG_CONVERT) --format=pdf --output=$@ $<

$(BUILD_DIR)/pulp-leaf-citrus-cell.pdf: assets/pulp-leaf-citrus-cell.svg
	@mkdir -p $(BUILD_DIR)
	$(RSVG_CONVERT) --format=pdf --output=$@ $<

presentation: $(BUILD_DIR)/pulp-mascot.pdf $(BUILD_DIR)/pulp-logo.pdf \
		$(BUILD_DIR)/pulp-leaves-cell.pdf $(BUILD_DIR)/pulp-citrus-cell.pdf \
		$(BUILD_DIR)/pulp-leaf-citrus-cell.pdf ## Live-preview the Beamer presentation
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(LATEXMK_FLAGS) \
		-pvc presentation.tex

presentation-build: $(BUILD_DIR)/pulp-mascot.pdf $(BUILD_DIR)/pulp-logo.pdf \
		$(BUILD_DIR)/pulp-leaves-cell.pdf $(BUILD_DIR)/pulp-citrus-cell.pdf \
		$(BUILD_DIR)/pulp-leaf-citrus-cell.pdf ## Build the Beamer presentation PDF
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(LATEXMK_FLAGS) \
		presentation.tex

draft: ## Live-preview the textual draft
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(LATEXMK_FLAGS) \
		-pvc draft.tex

draft-build: ## Build the textual draft PDF
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(LATEXMK_FLAGS) \
		draft.tex

speech-time: ## Estimate presentation speech time from draft sections
	@$(UV) run scripts/speech_time.py \
		--texcount $(TEXCOUNT) \
		--reference-time "$(REFERENCE_SECONDS)" \
		--switch-cost-seconds $(SWITCH_COST_SECONDS) \
		--watch $(WATCH) \
		draft.tex

format: ## Format LaTeX sources with latexindent
	@mkdir -p $(BUILD_DIR)
	$(LATEXINDENT) -wd -s \
		-c $(BUILD_DIR) \
		$(TEX_FILES)

clean: ## Remove generated build files
	$(LATEXMK) -C -outdir=$(BUILD_DIR) \
		presentation.tex draft.tex
	@rm -rf $(BUILD_DIR)
