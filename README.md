# wfpRainFinder

Steps for code challenge:

1) Set up development environment (download vs code, install conda, make conda env)
2) download data
3) extract relevant data for task 1 (rainFinder.py > findFiles)
4) compute 95th percentile rain for 1989-2019 for third dekad in March (rainFinder.py, get95thPercentile)
5) manipulate data for task 2 (convert raster pixels to points, make geodataframes, spatial join geodataframes, get mean rainfall per area)
6) set up submission of deliverables (write a summary, zip up files, move it all to github after)

Cloud Services Discussion

This is a several step process with many states to monitor (data downloads, processing, etc).  In AWS,
step functions would be a resource to orchestrate and monitor this workflow.  I have experience setting
up step functions via cloud formation.  A simple deployment would have a user execute the step function
on demand as needed (though this could be scheduled).  The cloud formation template would define security,
permissions, and those type of admin roles.  Those resources are created when the stack is published.
The template would also define, in a simple case, an on-demand EC2 instance that would handle processing.
The EC2 instance may be deployed with an image stored in an AWS Elastic Container Registry.  The image
would have the correct environment set up (python, conda environment, etc).  Outputs could be uploaded to
an S3 Bucket.  If the outputs needed to be accessed from a GUI/web app, an api could be created to access the
outputs on demand from the application.

More Info

I was time constrained on this one.  I did not really know what to expect for this assessment, so I did
not come to it from my usual, already set up development environment.  When I saw it was a code challenge 
I did have to spend time setting that up.  For step 3 I would have used geopandas to output a shapefile that 
contained the requested info.  A few calculations would have been added to a geodataframe which can easily
be written to a file.  For task 4, I would have taken the already calculated data and passed it through a 
numpy.where type filter to threshold the data and replace it with the binary mask.  Then, as described in
the instructions, multiply by population (all in a geodataframe) and output to a shapefile.
