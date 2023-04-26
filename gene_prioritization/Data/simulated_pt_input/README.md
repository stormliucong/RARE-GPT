### Simulate patient

- Collect HPO terms
- Create a pt by randomly adding HPO terms
- Do prediction for those random pts using GPT
- Calculate gene probability (null distribution) that GPT will predict for.
- Recalibrate the accuracy of the results
    - Sample genes top 5, top 10, top 50 based on null distribution
    - calculate the accuracy for different dataset