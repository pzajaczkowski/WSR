Instruction to create container for testing

```zsh
docker run -d --name=minicondor -v $(pwd)/jobs:/jobs htcondor/mini:latest
```
After that we need to compile estimate_pi.cpp but we need gcc:

```zsh
yum install -y gcc gcc-g++
g++ estimate_pi.cpp -o estimate_pi -O3
```

Then make sure to change user to be able to submit job:

```zsh
su - submituser
./execute.sh static-inputs.csv
```

If permission denied execute following inside `/jobs` in container

```zsh
chmod +777 * 
```

PS you can enter docker bash with:

```zsh
docker exec -it minicondor /bin/bash
```