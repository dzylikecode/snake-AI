# 
#
#
# - 注意要点
#   
#   要时常保持环境的更新, 所以需要install每个package后记录在environment.yml中
#
#
#
#
#
#


# get current directory name
cur_dir_name=${PWD##*/}             # to assign to a variable
cur_dir_name=${cur_dir_name:-/}     # to correct for the case where PWD=/
echo "current directory: $cur_dir_name"
repos_name=$cur_dir_name
echo "repository: $repos_name"

# project root
project_root=$(git rev-parse --show-toplevel)
env_file=$project_root/environment.yml
env_file_be_founded=0
if [ -f "$env_file" ]; then
    env_file_be_founded=1
    echo "environment file: $env_file"
fi

# function: create a new conda env
function create_conda_env() {
    echo "creating conda env: $1"
    if [ $env_file_be_founded -eq 1 ]; then
        conda env create -f $env_file
    else
        conda create -n $1 python=3.9
    fi
}

function remove_conda_env() {
    echo "removing conda env: $1"
    conda remove -n $1 --all
}

# command
alias dz_mk="create_conda_env $repos_name"
alias dz_rm="remove_conda_env $repos_name"
alias dz_cd="conda activate $repos_name"
# left
alias dz_lf="conda deactivate"    
# export env                    
alias dz_ex="conda env export -n $repos_name > $env_file"
# import
alias dz_im="conda env update -n $repos_name --file $env_file"
# install
function conda_install_package() {
    echo "installing package: $1"
    conda install -n $repos_name $1
    dz_ex
}
alias dz_in="conda_install_package"
# uninstall
function conda_uninstall_package() {
    echo "uninstalling package: $1"
    conda uninstall -n $repos_name $1
    dz_ex
}
alias dz_un="conda_uninstall_package"
# jupyter
alias dz_ipy="dz_in ipykernel"
# update
function conda_update_package() {
    echo "updating package: all"
    conda update -n $repos_name --all
    dz_ex
}
alias dz_up="conda_update_package"