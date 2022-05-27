declare -a StringArray=("../exasol-bucketfs-utils-python" )
python3 doc/call_pages_generator.py \
  --target_branch "github-pages/main" \
  --push_origin "origin" \
  --push_enabled "push" \
  --module_path "${StringArray[@]}" \
  --source_branch $(git tag --sort=committerdate | tail -1) \
  --source_origin "tags"


