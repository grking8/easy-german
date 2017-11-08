---
title: DevOps
order: 2
---

#### Step 1

Test build locally

- Build docker image; from project root `sudo docker build --tag=<name>:<tag> .`
- Run docker image `sudo docker run --detach --publish=80:80 --name=<containername> <imagename:imagetag>`
- Check `localhost` or `<ipaddress>` in browser.
- Stop container `sudo docker container stop <containername>`
- Delete container `sudo docker container rm <containername>`

#### Step 2

Deploy to production

- Push upstream.
- Wait for Docker Hub to build successfully.
- SSH into GCE instance; from home directory `./deploy-homepage.sh`
- Check `<productiondomain>` in browser.