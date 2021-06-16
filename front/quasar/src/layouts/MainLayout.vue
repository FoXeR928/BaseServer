<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar>
        <q-toolbar-title class="flex flex-center">
          <img style="max-width: 270px; padding: 20px" src="../assets/logo_niti.svg">
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container class="flex flex-center" style="margin: 50px 0">
      <section class="section-add_flask -section" id='all'>
            <nav>
                <q-btn align="center" class="btn-fixed-width" color="primary" label="Добавить флешку" />
                <q-btn align="center" class="btn-fixed-width" color="primary" label="Выдать флешку" />
                <q-btn align="center" class="btn-fixed-width" color="primary" label="Вернуть флешку" />
                <q-btn align="center" class="btn-fixed-width" color="primary" label="Найти флешку" />
            </nav>
            <form action="" method="GET">
              <div class="q-gutter-md">
                <q-input v-model="text" label="Поиск по имени" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="text" label="Поиск по id" />
              </div>
                <div></div>
            </form>
            <form class="q-gutter-md column items-start flex flex-center" method="POST">
              <q-input
                @input="val => { files = val }"
                multiple
                filled
                type="file"
                hint="Файл txt"
               />
              <q-input
                @input="val => { files = val }"
                multiple
                filled
                type="file"
                hint="Файл reg"
              />
              <q-btn align="center" class="btn-fixed-width" color="primary" label="Добавить" />
            </form>
            <form method="PUT">
              <div class="q-gutter-md">
                <q-input v-model="text" label="id флешки" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="text" label="ФИО получателя" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="text" label="Табельный номер получателя" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="text" label="Депортамет получателя" />
              </div>
              <div class="flex flex-center" style="margin: 20px">
                <q-btn align="center" class="btn-fixed-width" color="primary" label="Выдать" />
              </div>
            </form>
            <form method="PUT">
              <div class="q-gutter-md">
                <q-input v-model="text" label="id флешки" />
              </div>
              <div class="flex flex-center" style="margin: 20px">
                <q-btn align="center" class="btn-fixed-width" color="primary" label="Вернуть" />
              </div>
            </form>
        </section>
    </q-page-container>
  </q-layout>
</template>

<script>
  

export default {
  name: 'MainLayout',
  data () {
    return {
      leftDrawerOpen: false,
      essentialLinks: linksData
    }
  }
}
</script>
