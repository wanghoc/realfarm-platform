# AI Service

Separate Python service for model inference and training experiments.

## MVP candidate

Leaf disease classification with:

- model version;
- confidence;
- input image reference;
- evaluation metrics;
- manual-review threshold;
- retry-safe inference endpoint.

## Non-goals

The AI service must not:

- directly command actuators;
- decide chemical treatment without policy/expert review;
- claim production accuracy without evidence;
- store core lease or harvest ownership data.
