#/bin/bash

# Usage: ./make-train-valid.sh dir_containing_labels number_of_valids
#
# dir_containing_labels contains subdirectories lable1, label2..., each containing files of the corresponding label.
# number_of_valids is the number of validations to use for each label
#
# Example Usage: ./make-train-valid.sh catsdogs 100

if [ "$#" -ne 2 ]; then
    echo "use: $0 dir_containing_labels number_of_valids";
    exit
fi

dir=$1; num_valid=$2

cd $dir
path=`pwd`
sdirs='valid train'
rm -fr $sdirs
labels=`ls`
mkdir $sdirs

split() {
    lab=$1
    files=`ls $lab/ |shuf`
    total=`echo $files|wc -w`
    num_train=$(($total - $num_valid))
    valid=`echo $files|tr ' ' '\n' | head -$num_valid`
    train=`echo $files|tr ' ' '\n' | tail -$num_train`
    
    mkdir $path/valid/$lab
    for f in $valid; do
	cp "$path/$lab/$f" $path/valid/$lab/.
    done

    mkdir $path/train/$lab
    for f in $train; do
	cp "$path/$lab/$f" $path/train/$lab/.
    done
    
}

for lab in $labels;do
    split $lab
done
