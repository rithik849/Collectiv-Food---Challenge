
**How to run the application?**

To run the app using docker ensure that the my-volume directory is a trusted folder in Docker. 

To check this in Docker Hub go to Settings/Resources/FileSharing and add the path to the Virtual File Shares.

To set up the application, run this in the backend directory:

```Shell
docker compose up
```

This will allow for the frontend to be accessible on http://localhost:8080 and the backend on http://localhost:8000

**Assumptions**

When desinging the application, I assumed that the order id will be generated on the application end rather than input by the user. As well as this as there was no price allocated for each product, this was left to the user to input in the frontend.

**Design Decisions**

In the frontend form I included the products as a choice among products to prevent the accidental inclusion of items that do not exist.

As well as this I ensured that once a product was chosen in the form it could not be added as another entry to prevent duplication and different prices being input for the same product.

In the backend, I kept the validation logic in its own package seperate from the backend to keep the application more maintainable, seperating the backend server logic from the data validation logic.

**Future Additions**

If given more time I would add the following:

Include an option to apply discounts for customers with codes.

Can include tighter validation for the address, for example using a google maps api to ensure the address matches the business address.

Could also include an agent that allows users to decide what products to buy according to more complex needs, such as if a restaurant is holding an offer to sell a popular set of dishes, the AI agent can help with deciding what ingredients would need to be stocked up.
