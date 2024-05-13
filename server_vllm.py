#Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("sentiment-analysis")
print(pipe(["go away bozo"]))
#pipelines can detct sentiment

#this presents the case for moderation
