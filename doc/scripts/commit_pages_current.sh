declare -a StringArray=("../exasol-bucketfs-utils-python" )
python3 doc/call_pages_generator.py \
  --target_branch "github-pages/"$(git branch --show-current)"" \
  --push_origin "origin" \
  --push_enabled "commit" \
  --module_path "${StringArray[@]}"

