# A plain-language guide to this experiment

This is an assisted study guide, not a record of the student's own explanation.

The model practices finishing sentences. For example, the teaching material has
many sentences about a customer ordering or reviewing a product. The model tries
to predict the next word, compares its prediction with the word actually in the
sentence, and adjusts its internal numbers. Repeating that process is training.

## Start with one word

`customer` is a **token**, a piece of text. In the starter run, its **ID is 28**.
That ID is just a lookup number, like a page number. It does not mean that
customer has a quantity or meaning of 28.

The lookup retrieves an **embedding**, a row of 64 numbers. The model uses those
numbers in its calculations. Training can change those numbers. Individual
coordinates are not named concepts such as kindness, price, or intelligence.

## Then make a guess

The model combines the information from the words it has seen and assigns a
**probability** to every possible next token. After training, one example is
“the customer” → a 17.8% probability for “reviewed.” That is a prediction about
the next word, not a score for whether a claim is true.

**Attention** is part of how the model uses earlier words. It can combine
information from earlier positions in the sentence, but it cannot peek at the
future word it is supposed to predict.

## Learn from the prediction

**Loss** is a measure of prediction error. Giving the actual next word a very
low probability causes a larger loss. A **gradient** describes which direction
of change to an internal number would locally increase or decrease the loss.
The optimizer uses gradients to make small **weight updates**.

In this run, the first update changed one number from −0.0575919 to −0.0576019.
One tiny change is not the whole lesson: thousands of updates together changed
later predictions. The actual optimizer uses clipping, momentum, adaptive
scaling, and weight decay, so it is more complicated than multiplying the
displayed gradient by 0.001.

## Check learning fairly

Training examples are practice material. Validation passages are set aside and
do not supply weight updates. The 48 fixed tests are a separate development
benchmark. Feeding their stories or answer keys into training would make the
comparison misleading.

Our model became better at familiar patterns, but both newly scorable opposites
tests were still wrong. This shows why adding words and lowering loss do not
prove that the model understands the relationship being tested.

**Temperature** changes how adventurous sampling is after training. It changes
which words might be selected from the learned probabilities, not the weights
or what the model has learned.

## Explain one idea at a time

Try finishing these sentences in your own words. These are prompts for a future
learning conversation, not answers attributed to the student:

1. “The corpus is …”
2. “An ID points to …, while an embedding is …”
3. “During training, the model changes … because …”
4. “A good four-choice score can still come with a bad reply because …”
5. “Increasing temperature changes … but does not change …”
