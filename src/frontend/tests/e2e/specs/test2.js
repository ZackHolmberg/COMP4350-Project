// https://docs.cypress.io/api/introduction/api.html

describe('After loading the app', () => {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080)
    })

    it('Successfully logs into the app and navigates to home page', () => {
      cy.visit('http://localhost:8080/')
      cy.get('#username').type('Username') 
      cy.get('#password').type('Password') 
      cy.get('#button').click()   
      cy.url().should('eq', 'http://localhost:8080/home')
    })
  })
  
})


