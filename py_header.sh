#!/usr/bin/env bash
# Add a shebang and a simple docstring to all python files in the workspace

work_files=$(find . -name "*.py" -type f)

for file in $work_files
do
    if [[ -s "$file" ]]
    then
        if head -1 "$file" | grep -qvE '^#!'
        then
            sed -Ei -e '1i\#!/usr/bin/python3' \
                -e "1i\"\"\"Module for $(basename -s .py $file).\"\"\"" \
                "$file"
        fi
    else
        echo '#!/usr/bin/python3' > "$file" &&
        echo '"""Module for '"$(basename -s .py $file)"'."""' >> "$file"
    fi

    chmod u+x "$file"
done
