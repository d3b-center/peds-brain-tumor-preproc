## Intended for CHOP-D3b use

This Docker container is a pre-processing module for the CHOP-D3b pediatric brain tumor pipeline. It uses the CaPTk Docker container with version 1.8.1 as the base image.

### Building the container

From within the directory, build on your local machine:

```
docker build -t afam00/peds-brain-tumor-preproc:1.0.0 .
```

The container can then be pushed to Docker Hub for public release. Don't forget to also update the corresponding Docker tag in the public `docker-compose.yml` ().

```
docker push afam00/peds-brain-tumor-preproc:1.0.0
```

### Running

When built/pulled locally, the container can be run:

```
docker run --rm peds-brain-tumor-preproc
```

or

```
docker run -it --entrypoint='' peds-brain-tumor-preproc bash
```

### Notes

### Limitations
