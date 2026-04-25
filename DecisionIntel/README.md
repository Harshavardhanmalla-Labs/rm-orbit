# Decision Intelligence MVP

React-based decision guidance system with prediction intelligence and user feedback collection.

## Setup

```bash
npm install
npm run dev
```

Opens on `http://localhost:5173`

## Architecture

- **Home**: Dashboard with CTA
- **Decide**: Decision input with optional context
- **PredictionResult**: Prediction display (high/low confidence modes)
- **DecisionConfirmation**: Decision recorded confirmation
- **FeedbackModal**: Post-decision feedback (6 questions)

## Coaching Mode (Confidence < 0.60)

- Honest uncertainty messaging
- Primary: "Go with recommendation"
- Secondary: "I'll decide myself"
- Progressive disclosure for details

## Tracking

All events logged to console. Events tracked:
- `decision_started`
- `context_added`
- `decision_submitted`
- `prediction_vs_user_choice`
- `scroll_depth`
- `hesitation_detected`
- `low_confidence_details_expanded`
- `feedback_*`

## Mock Data

Prediction confidence ranges 0.20–1.0. Coaching mode triggers when confidence < 0.60.

## No Backend Required

All data is ephemeral. No persistence.
