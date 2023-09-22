# A rewritten insider Dockerfile

This clones and builds https://github.com/ZupIT/horusec

## Why?

Because we needed to minimize the size of the original image and all the images that get pulled.

```
horuszup/horusec-cli                           latest          12639d8878e2   15 months ago    256MB
horuszup/horusec-ruby                          v1.2.0          454782d7c4a0   18 months ago    92.3MB
horuszup/horusec-generic                       v1.2.0          0c8451f6c1bd   18 months ago    351MB
horuszup/horusec-shell                         v1.0.1          0008b86a0bb5   22 months ago    19.5MB
horuszup/horusec-c                             v1.0.1          1262af420c8d   22 months ago    52.1MB
```

This image is only 100MB.

```
horusec                                        2.8.0           9eabb68d6ca9   4 minutes ago    109MB
```

We also add a customized / normalized report fitting to our needs.

## How?

### Build

```bash
docker build . -t horusec:2.8.0 # or whatever you wanna call it
```

### Run

It is preferable to mount the `/data` folder as shown with your current project's folder in order to receive a proper `report.insider.json` file as an output.

```bash
docker run -v $(pwd):/data --rm horusec:2.8.0 -p /data
```

This will copy the two report files to your mounted folder. \
Keep in mind that insider may scan all files. Some extentions have been excluded in the example.
