# Prompts — explicit LLM cartographer artifacts

Adapted from the `tvoo_backend/prompts/` pattern in the
programmeerprobeer project, scaled for one-off research use.

## What this folder is

Every time we use an LLM as part of the research workflow, the prompt
lives here as an explicit YAML artifact — versioned, reviewable,
diffable. Not embedded in script code, not improvised in a chat.

## Why

The project's discipline (from
[import-feature-sketch §2](../../../../research/import-feature-sketch.md))
is **"LLM is the cartographer, not the driver"**:

- The LLM helps *design the mapping* (build the dictionary, propose
  the categorisation rules, suggest the schema).
- Plain code *applies the mapping* deterministically to every row.

Capturing the prompts as files lets us:

- **Re-run reproducibly** if the input changes (more notes, revised
  category set) → re-run the prompt, regenerate the dictionary, diff
  the output.
- **Iterate on the prompt itself** with version numbers (`_v1`,
  `_v2`), keeping prior versions for comparison.
- **Review what was asked of the LLM** without hunting through code or
  conversation history.

## Difference from the tvoo_backend pattern

- **No LangChain runtime here.** tvoo_backend is a production backend
  that loads prompts via `langchain.PromptTemplate.from_yaml()` and
  pipes them to a chat model. For research, the agent (Claude / GPT
  in conversation) reads the YAML and produces the output directly.
- **Output is committed alongside the prompt** so the link
  prompt → output is auditable.
- **Lighter ceremony**: no `_type`, no `output_parser`, no
  `input_variables` list if the variables are obvious from the
  template body — although for non-trivial prompts the list is still
  useful.

## File naming

Mirror tvoo's convention:

`<task>_<version>.yaml` — e.g. `category_dictionary_seed_v1.yaml`.

Never edit a prompt that has produced shipped output; bump to `_v2`.

## Workflow per prompt

1. **Author** the prompt YAML in this folder. Include in the template:
   the task, the inputs (as `{placeholder}` style), the expected
   output shape, any constraints.
2. **Render** the prompt by substituting actual input values
   (manually fine for research; a tiny helper if it gets repetitive).
3. **Run** the rendered prompt against the agent. Capture the agent's
   full response.
4. **Commit** the output as a separate file in the parent folder
   (`../category_dictionary.md`, `../category_dictionary.yaml`,
   etc.) so prompt → output is a single PR-able pair.
5. **Note in the parent folder's README** which prompt produced
   which output, and which agent / model was used.

## Current prompts in this folder

| file | task | output |
|------|------|--------|
| `category_dictionary_seed_v1.yaml` | Build the seed phrase dictionary for clause-level categorisation of Dutch Long-COVID journal notes. | `../category_dictionary.md` (to be converted to `.yaml` once finalised by user review) |
