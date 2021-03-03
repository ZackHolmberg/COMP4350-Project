describe('Checks nav bar', () => {
    context('1080p resolution', () => {
      beforeEach(() => {
        // run these tests as if in a desktop
        cy.viewport(1920, 1080)
        cy.visit('http://localhost:8080/')
        cy.get('#username').type('Username') 
        cy.get('#password').type('Password') 
        cy.get('#button').click()
      })
 
      it('Nav bar icons are visible', () => {   
        cy.url().should('eq', 'http://localhost:8080/home')  
        cy.get('#nav-logo').should('be.visible') 
        cy.get('#nav-account').should('be.visible')
        cy.get('#nav-settings').should('be.visible')
        cy.get('#nav-logout').should('be.visible')   
      })
    })
  })

  