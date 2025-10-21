import asyncio
import os
from aiohttp import web, ClientSession

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
# URL du serveur A (à modifier selon ton hébergement)
SERVER_A_URL = "https://bot-spet.onrender.com/ping"  # exemple : URL publique de A

# ----------------------------------------------------------------------
# SERVEUR HTTP DE B
# ----------------------------------------------------------------------
async def handle_ping(request):
    """Réception d'un ping venant du serveur A"""
    data = await request.json()
    print(f"[B] Reçu de A : {data}")
    return web.json_response({"message": "pong from B"})

async def keep_alive_server():
    """Démarre le serveur HTTP de B"""
    app = web.Application()
    app.router.add_post("/ping", handle_ping)
    app.router.add_get("/", lambda request: web.Response(text="Server B is running."))

    PORT = int(os.environ.get("PORT", 5001))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌐 Serveur B démarré sur 0.0.0.0:{PORT}")

# ----------------------------------------------------------------------
# ENVOI DE PING VERS A
# ----------------------------------------------------------------------
async def ping_a_loop():
    """Envoie un ping toutes les 20 secondes à A"""
    async with ClientSession() as session:
        while True:
            try:
                payload = {"from": "B"}
                print("[B] Envoi à A :", payload)
                async with session.post(SERVER_A_URL, json=payload, timeout=10) as resp:
                    response = await resp.json()
                    print("[B] Réponse de A :", response)
            except Exception as e:
                print("[B] Erreur :", e)
            await asyncio.sleep(20)

# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
async def main():
    asyncio.create_task(keep_alive_server())  # Démarre le serveur HTTP
    asyncio.create_task(ping_a_loop())        # Lance la boucle de ping
    while True:  # empêche le script de se fermer
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
