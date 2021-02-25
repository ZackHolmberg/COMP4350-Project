// https://docs.cypress.io/api/introduction/api.html

describe('Loads the web app', () => {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      // browser with a 1080p monitor
      cy.viewport(1920, 1080)
    })

    it('Visits the app root url', () => {
      cy.visit('http://localhost:8080/')
      cy.get('[alt="BisonCoin logo"]')
      .should('be.visible')    })
  })
  
})


