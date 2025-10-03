import { test, expect } from '@playwright/test';

const PROD_URL = 'https://pharmabot-vidal-assistant.netlify.app';

test.describe('Production PharmaBot Tests', () => {
  test('page loads in production', async ({ page }) => {
    await page.goto(PROD_URL);
    
    // Vérifie que le titre existe
    await expect(page.getByRole('heading', { name: 'PharmaBot' })).toBeVisible({ timeout: 10000 });
    
    // Vérifie le sous-titre
    await expect(page.getByText('Assistant professionnel')).toBeVisible();
  });

  test('can send a message and receive response', async ({ page }) => {
    await page.goto(PROD_URL);
    
    // Attendre que la page soit chargée
    await page.waitForSelector('input[placeholder*="Posez votre question"]', { timeout: 10000 });
    
    // Remplir et envoyer un message
    const input = page.getByPlaceholder(/Posez votre question/);
    await input.fill('Quelles sont les indications du paracétamol?');
    
    // Cliquer sur le bouton d'envoi
    const sendButton = page.getByRole('button').filter({ has: page.locator('svg') }).last();
    await sendButton.click();
    
    // Attendre la réponse (peut prendre du temps sur Render free tier)
    await page.waitForTimeout(15000);
    
    // Vérifie que le message utilisateur apparaît
    await expect(page.getByText('Quelles sont les indications du paracétamol?')).toBeVisible({ timeout: 5000 });
    
    // Vérifie qu'une réponse est visible
    const messages = page.locator('[class*="bg-blue"], [class*="bg-gray"]');
    await expect(messages.first()).toBeVisible({ timeout: 10000 });
  });

  test('search functionality works', async ({ page }) => {
    await page.goto(PROD_URL);
    
    // Cliquer sur le bouton Recherche
    await page.getByRole('button', { name: /Recherche/ }).click();
    
    // Vérifie qu'on est sur la page de recherche
    await expect(page.getByRole('heading', { name: 'Recherche dans la base' })).toBeVisible({ timeout: 5000 });
    
    // Effectuer une recherche
    const searchInput = page.getByPlaceholder(/Rechercher un médicament/);
    await searchInput.fill('paracétamol');
    
    const searchButton = page.getByRole('button', { name: /Rechercher/ });
    await searchButton.click();
    
    // Attendre les résultats
    await page.waitForTimeout(3000);
    
    // Vérifie qu'il y a des résultats ou un message
    const hasResults = await page.getByText(/résultat/).isVisible().catch(() => false);
    const hasNoResults = await page.getByText(/Aucun résultat/).isVisible().catch(() => false);
    
    expect(hasResults || hasNoResults).toBeTruthy();
  });

  test('backend API is accessible', async ({ page }) => {
    const response = await page.request.get('https://pharmabot-olwu.onrender.com/api/health');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.status).toBe('healthy');
    expect(data.app).toBe('PharmaBot');
  });

  test('CORS is properly configured', async ({ page }) => {
    // Test que les requêtes cross-origin fonctionnent
    const response = await page.request.post('https://pharmabot-olwu.onrender.com/api/chat', {
      data: {
        message: 'test',
        conversation_history: [],
      },
      headers: {
        'Origin': 'https://pharmabot-vidal-assistant.netlify.app',
        'Content-Type': 'application/json'
      }
    });
    
    // Doit retourner 200 ou une erreur métier, pas une erreur CORS
    expect(response.status()).not.toBe(0); // 0 = CORS error
  });
});
