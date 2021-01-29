# place-review-system
An overhaul of the current review system, enabling useful feedback through datapoints for hospitality venues 

## TODO:
- Views overhaul
- Scorecard
  - Constraints
  - Testing
- View testing
- Move away from w3.css and implement custom sass for UI
- Search function to filter front page queryset
  - Connect with google places api to pull venue details if they do not exist.

## Considerations"
- Consider what data to keep when users/reviews/venues are deleted
- Crossovers in place attributes?
  - Food/Drink and Quality
  - Perhaps add variety and remove quality
- Refactor review.html to remove repetition, need to reference and loop through Feedback model field names
