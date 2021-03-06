describe('On the mining component', () => {
    context('1080p resolution', () => {
      beforeEach(() => {
        // run these tests as if in a desktop
        // browser with a 1080p monitor
        cy.viewport(1920, 1080)
        cy.visit('http://localhost:8080/')
        cy.get('#username').type('Username') 
        cy.get('#password').type('Password') 
        cy.get('#button').click()
      })
  
      it('Validates that the mining component is visible and value is as expected', () => {
        cy.url().should('eq', 'http://localhost:8080/home')
        mining = cy.get('[id="mining"]')
        mining.should('be.visible')    
        mining.contains("Mining On") 
        mining.click()
        mining.contains("Mining Off")
      }) 
    })  
  })