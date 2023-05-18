docker build -t my-first-image:latest .

# Because I used AWS's python image,
#   From `Test an image with RIE included in the image` at https://docs.aws.amazon.com/lambda/latest/dg/images-test.html I can run the emulator.
#   The below runs the docker container's port 8080 locally on port 9000, which makes an invocation endpoint
#   the -v option mounts the downloads directory on my host machine to the docker's /data directory, which I made in the dockerfile
docker run -v ~/Downloads:/data -p 9000:8080 my-first-image:latest
# Then in a separate shell, I can run this command to post my local event file data to the invocation endpoint
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d @local_event.json > output.json
