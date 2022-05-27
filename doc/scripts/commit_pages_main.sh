declare -a StringArray=("../exasol-bucketfs-utils-python" )
python3 doc/call_pages_generator.py \
  --target_branch "github-pages/main" \
  --push_origin "origin" \
  --push_enabled "commit" \
  --source_branch "main"  \
  --module_path "${StringArray[@]}"

