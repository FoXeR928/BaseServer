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
                <q-btn v-on:click="show = true, show_search = false, show_get = false, show_give = false" align="center" class="btn-fixed-width" color="primary" label="Добавить флешку" />
                <q-btn v-on:click="show_give = true, show_search = false, show = false, show_get = false" align="center" class="btn-fixed-width" color="primary" label="Выдать флешку" />
                <q-btn v-on:click="show_get = true, show_search = false, show = false, show_give = false" align="center" class="btn-fixed-width" color="primary" label="Вернуть флешку" />
                <q-btn v-on:click="show = false, show_search = true, show_get = false, show_give = false" align="center" class="btn-fixed-width" color="primary" label="Найти флешку" />
            </nav>
            <form v-if="show_search" action="" method="GET">
              <div class="q-gutter-md">
                <q-input v-model="fio" label="Поиск по имени" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="tabnum" label="Поиск по табельному номеру" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="device_id" label="Поиск по id" />
              </div>
              <div></div>
            </form>
            <form v-if="show" class="q-gutter-md column items-start flex flex-center" style="margin: 1px 0" method="POST">
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
            <form v-if="show_give" method="PUT">
              <div class="q-gutter-md">
                <q-input v-model="device_id" label="id флешки" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="fio" label="ФИО получателя" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="tabnum" label="Табельный номер получателя" />
              </div>
              <div class="q-gutter-md">
                <q-input v-model="department" label="Депортамет получателя" />
              </div>
              <div class="flex flex-center" style="margin: 20px">
                <q-btn align="center" @click="give_flask(device_id, fio, tabnum, departament)" class="btn-fixed-width" color="primary" label="Выдать" />
              </div>
            </form>
            <form v-if="show_get" method="PUT">
              <div class="q-gutter-md">
                <q-input v-model="device_id" label="id флешки" />
              </div>
              <div class="flex flex-center" style="margin: 20px">
                <q-btn align="center" @click="get_flask(device_id)" class="btn-fixed-width" color="primary" label="Вернуть" />
              </div>
            </form>
        </section>
    </q-page-container>
  </q-layout>
</template>

<script> 
import axios from 'axios'
export default {
 
  
  data(){
    return{
      device_id: '',
      fio: '',
      tabnum: '',
      department: '',
      show_search: true,
      show: false,
      show_give: false,
      show_get: false,
    }
  },
  methods: {
    get_flask(device_id){
      return axios.put("/get_flask", {
        content: device_id
      })
    },
    give_flask(device_id, fio, tabnum, departament){
      return axios.put("/give_flask",{
        content: device_id, fio, tabnum, departament
      })
    }
  }
} 
</script>