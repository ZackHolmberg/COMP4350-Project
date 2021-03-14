describe("App Login", () => {
  context("1080p resolution", () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080);
      cy.visit("http://localhost:8080/");
    });

    it("Successfully logs into the app and navigates to home page", () => {
      cy.get("#umnetId").type("umnetId");
      cy.get("#password").type("Password");
      cy.intercept("POST", "/users/login", { fixture: "loginSuccess.json" }).as(
        "userLogin"
      );
      cy.intercept("POST", "/wallet/amount", {
        fixture: "walletAmountEmpty.json",
      }).as("getWalletAmount");
      cy.get("#login-button").click();
      cy.wait(["@userLogin"]);
      cy.wait(["@getWalletAmount"]);
      cy.url().should("eq", "http://localhost:8080/home");
    });

    it("Displays empty field toast when trying to login with one empty input field", () => {
      cy.get("#umnetId").type("umnetId");
      cy.get("#login-button").click();
      transaction = cy.get('[class="v-toast__text"]');
      transaction.should("be.visible");
      transaction.contains(
        "One or more input fields are empty. Please fill out all input fields."
      );
    });

    it("Displays error toast when trying to login and login error occurs", () => {
      cy.get("#umnetId").type("umnetId");
      cy.get("#password").type("Password");
      cy.intercept("POST", "/users/login", {
        statusCode: 400,
        body: {
          error: "An error occured!",
        },
      }).as("userLogin");
      cy.get("#login-button").click();
      cy.wait(["@userLogin"]);
      transaction = cy.get('[class="v-toast__text"]');
      transaction.should("be.visible");
      transaction.contains("An error occured!");
    });
  });
});
