from playwright.sync_api import sync_playwright
from config import EMAIL, PASSWORD, URL_OCC
import time
import pdb

TIME_OUTS = 2000
JOB_SEARCH = 'data' # tipo de trabajo que quieres buscar ejemplo: data, QA, testing, etc.
MIN_SALARY = 50000 # Salario minimo para filtrar los trabajos

def main():
    with sync_playwright() as p:

        # Bucle para cada email
        for idx, email in enumerate(EMAIL):
            # 1. Abrir navegador (modo visible para ver qué pasa)
            browser = p.chromium.launch(
                headless=False,  # True cuando ya funcione
                slow_mo=200,
                args=["--window-size=1080,720"]
            )

            # Crear contexto sin viewport para maximizado
            context = browser.new_context(no_viewport=True)
            print(f"\n{'=' * 50}")
            print(f"📧 Procesando EMAIL_{idx}: {email}")
            print(f"{'=' * 50}")

            # 2. Crear página
            page = context.new_page()

            # 3. Navegar a OCC Mundial
            print(f"🌐 Navegando a {URL_OCC}...")
            page.goto(URL_OCC)

            page.locator("#login-link").click()
            page.locator("#inputID_identifier").click()
            page.locator("#inputID_identifier").fill(email)  # Usar el email actual
            page.locator("#inputID_password").click()
            page.locator("#inputID_password").fill(PASSWORD)
            page.get_by_role("button", name="Iniciar sesión").click()
            page.wait_for_timeout(TIME_OUTS + 1000)

            page.goto(
                f"https://www.occ.com.mx/empleos/de-{JOB_SEARCH}/trabajo-en-tecnologias-de-la-informacion-sistemas/tipo-home-office-remoto?smin={MIN_SALARY}")
            page.wait_for_timeout(TIME_OUTS + 1000)

            procesar_todas_las_paginas(page)

            # Cerrar la página después de procesar este email
            page.close()

            # Cerrar el navegador después de todos los emails
            browser.close()


def procesar_todas_las_paginas(page):
    """Procesa todas las páginas detectando cuando el botón está deshabilitado"""
    pagina_actual = 1
    max_paginas = 50

    while pagina_actual <= max_paginas:
        print(f"\n{'=' * 50}")
        print(f"📄 PROCESANDO PÁGINA {pagina_actual}")
        print(f"{'=' * 50}")

        # Procesar trabajos de la página actual
        try:
            click_a_trabajos_no_postulados(page)
        except Exception as e:
            print(f"❌ Error procesando trabajos: {e}")
            # pdb.set_trace()
            # return

        # Buscar botón siguiente
        next_button = page.locator("#btn-next-offer")

        # Verificar si el botón está deshabilitado por la clase CSS
        if next_button.count() > 0:
            # Verificar si tiene la clase que lo deshabilita
            has_pointer_events_none = next_button.get_attribute("class")

            if "pointer-events-none" in has_pointer_events_none:
                print("🔚 Botón 'Siguiente' está deshabilitado (clase pointer-events-none)")
                print("🏁 Última página alcanzada")
                return

            # También verificar si está visible (por si acaso)
            if not next_button.is_visible():
                print("🔚 Botón 'Siguiente' no está visible")
                return

        # Hacer clic para ir a siguiente página
        try:
            print(f"➡️ Haciendo clic en página {pagina_actual + 1}...")
            next_button.click()

            # Esperar a que la página cargue
            page.wait_for_timeout(2500)
            pagina_actual += 1

        except Exception as e:
            print(f"❌ Error al hacer clic en siguiente página: {e}")
            # pdb.set_trace()
            return

    print(f"\n✨ Proceso completado. Total páginas procesadas: {pagina_actual}")

def click_a_trabajos_no_postulados(page):
    """
    Da click a todos los job cards que NO tengan el span de "Ya estás postulado"
    """
    # 1. Encontrar TODOS los job cards usando el patrón del ID
    todos_los_trabajos = page.locator('[id^="jobcard-"]')  # Todos los que empiezan con "jobcard-"
    total_trabajos = todos_los_trabajos.count() - 3
    print(f"📊 Total de trabajos encontrados: {total_trabajos}")
    contador_aplicados = 0
    contador_omitidos = 0
    # 2. Recorrer cada trabajo
    for i in range(total_trabajos):
        try:
            trabajo = todos_los_trabajos.nth(i)
            job_id = trabajo.get_attribute('id')
            print(f"\n🔍 Revisando trabajo {i + 1}/{total_trabajos}: {job_id}")
            trabajo.click()
            page.wait_for_timeout(TIME_OUTS)
            # Verificar si el elemento está visible
            if page.locator("#btn-apply").is_visible():
                print(f"   ✅ NO postulado - dando click...")
                page.locator("#btn-apply").click()
                page.wait_for_timeout(TIME_OUTS)
                click_todos_los_expertos_simple(page)
                page.wait_for_timeout(TIME_OUTS)
                try:
                    page.get_by_role("button", name="Postularme").click()
                    contador_aplicados += 1
                except Exception as e:
                    print(f"⚠️ Boton no encontrado {'name="Postularme"'}: {e}")
                    contador_aplicados += 1
                    # pdb.set_trace()
            else:
                print(f"   ⏭️  YA POSTULADO - omitiendo")
                contador_omitidos += 1
        except Exception as e:
            print(f"⚠️ Error en job id {job_id}: {e}")
            # pdb.set_trace()
    # 5. Resumen
    print(f"\n{'=' * 40}")
    print(f"✅ RESUMEN:")
    print(f"   Total trabajos: {total_trabajos}")
    print(f"   Click dados: {contador_aplicados}")
    print(f"   Omitidos (ya postulados): {contador_omitidos}")
    print(f"{'=' * 40}")


def click_todos_los_expertos_simple(page):
    """
    Da click a TODOS los botones Experto UNA SOLA VEZ cada uno
    """
    clicks = 0
    # Obtener TODOS los botones actuales
    botones = page.get_by_role("button", name="Experto")
    total_botones = botones.count()
    print(f"   🔍 Encontrados {total_botones} botones Experto")
    # Click a cada botón UNA SOLA VEZ
    for i in range(total_botones):
        try:
            boton = botones.nth(i)
            if boton.is_visible():
                boton.scroll_into_view_if_needed()
                page.wait_for_timeout(TIME_OUTS+(-int(TIME_OUTS*0.8)))
                boton.click()
                clicks += 1
                print(f"      ✓ Click Experto #{clicks}")
                page.wait_for_timeout(TIME_OUTS+(-int(TIME_OUTS*0.8)))  # Esperar que procese
        except Exception as e:
            print(f"      ⚠️ Error en botón {i}: {e}")
            # pdb.set_trace()
    print(f"   ✅ Total clicks a Experto: {clicks}")
    return clicks
if __name__ == "__main__":
    print("🚀 Iniciando CrackingTheOCCMundial")
    main()