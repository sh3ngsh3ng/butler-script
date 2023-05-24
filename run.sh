#! /bin/bash

echo "You have selected $2 from $1" 
script_name=$2
script_extension=${script_name##*.}


if [ "$script_extension" == "sh" ]; then
    echo "Bash script identified"
    sleep 1
    echo "Running $script_name"
    bash "./$1/$2"
elif [ "$script_extension" == "js" ]; then
    echo "Node script identified"
    sleep 1
    echo "Running $script_name"
    node "./$1/$2"
elif [ "$script_extension" == "py" ]; then
    echo "Python script identified"
    sleep 1
    echo "Running $script_name"
    py "./$1/$2"
else
    echo "Unknown file"
fi

if [ "$?" == 0 ]; then
    echo "Script executed successfully"
else
    echo "Script failed to execute"
fi

exit



