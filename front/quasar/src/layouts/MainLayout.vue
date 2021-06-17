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
                <q-btn v-on:click="show = false, show_all = true, show_get = false, show_give = false, show_search=false" align="center" class="btn-fixed-width" color="primary" icon="home" />
                <q-btn v-on:click="show = true, show_all = false, show_get = false, show_give = false, show_search=false" align="center" class="btn-fixed-width" color="primary" label="Добавить флешку" />
                <q-btn v-on:click="show_give = true, show_all = false, show = false, show_get = false, show_search=false" align="center" class="btn-fixed-width" color="primary" label="Выдать флешку" />
                <q-btn v-on:click="show_get = true, show_all = false, show = false, show_give = false, show_search=false" align="center" class="btn-fixed-width" color="primary" label="Вернуть флешку" />
                <q-btn v-on:click="show = false, show_all = false, show_get = false, show_give = false, show_search=true" align="center" class="btn-fixed-width" color="primary" label="Найти флешку" />
            </nav>
            <form v-if="show_all" action="" method="GET">
              <q-input bottom-slots v-model="fio" label="Поиск по имени">
                <template v-slot:append>
                  <q-icon v-if="fio !== ''" name="close" @click="fio = ''" class="cursor-pointer" />
                </template>
                <template v-slot:after>
                  <q-btn @click="search_device_fio(fio)" round dense flat icon="send" />
                </template>
              </q-input>
              <q-input bottom-slots v-model="tabnum" label="Поиск по табельному номеру">
                <template v-slot:append>
                  <q-icon v-if="tabnum !== ''" name="close" @click="tabnum = ''" class="cursor-pointer" />
                </template>
                <template v-slot:after>
                  <q-btn @click="search_device_tabnum(tabnum)" round dense flat icon="send" />
                </template>
              </q-input>
              <q-input bottom-slots v-model="device_id" label="Поиск по id">
                <template v-slot:append>
                  <q-icon v-if="device_id !== ''" name="close" @click="device_id = ''" class="cursor-pointer" />
                </template>
                <template v-slot:after>
                  <q-btn @click="search_device_id(device_id)" round dense flat icon="send" />
                </template>
              </q-input>
              <div>{{result}}</div>
            </form>
            <form v-if="show" class="q-gutter-md column items-start flex flex-center" style="margin: 1px 0" method="POST">
              <q-input
                @input="val => { files = val }"
                multiple
                filled
                v-model="file_txt"
                type="file"
                hint="Файл txt"
               />
              <q-input
                @input="val => { files = val }"
                multiple
                filled
                v-model="file_reg"
                type="file"
                hint="Файл reg"
              />
              <q-btn align="center" @click="add_flask(file_txt, file_reg)" class="btn-fixed-width" color="primary" label="Добавить" />
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
                <q-input v-model="departament" label="Депортамет получателя" />
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
            <form action="" method="GET" v-if="show_search">
              
              <div class="q-gutter-md">
                <q-input v-model="device_id" label="id флешки" />  
              </div>
              <div class="flex space-between" style="justify-content: space-between; margin: 10px 0;">
                <q-btn @click="search_date(device_id)" align="center" class="btn-fixed-width" color="primary" label="Поиск данных флешки" />
                <q-btn @click="search_off()" align="center" class="btn-fixed-width" color="primary" label="Списанные флешки" />
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
      file_txt: '',
      file_reg: '',
      fio: '',
      tabnum: '',
      departament: '',
      result: axios.get("/all_flask"),
      show_all: true,
      show_search: false,
      show: false,
      show_give: false,
      show_get: false,
    }
  },
  methods: {
    add_flask(file_txt, file_reg){
      return axios.post("/add_flask",{
        content: file_txt, file_reg
      })
    },
    get_flask(device_id){
      return axios.put("/get_flask", {
        content: device_id
      },{
      headers: {
        'Content-type': 'application/json',
      }
      })
    },
    give_flask(device_id, fio, tabnum, departament){
      return axios.put("/give_flask",{
        content: device_id, fio, tabnum, departament
      },
      {
      headers: {
        'Content-type': 'application/json',
      }
      })
    },
    search_device_fio(fio){
      return axios.get("/name_flask",{
        content: fio
      },
      {
      headers: {
        'Content-type': 'application/json',
      }
      })
    },
    search_device_tabnum(tabnum){
      return axios.get("/tabnum_flask",{
        content: tabnum
      },
      {
      headers: {
        'Content-type': 'application/json',
      }
      })
    },
    search_device_id(device_id){
      return axios.get("/id_flask?device_id="+ device_id,
      {
      headers: {
        'Content-type': 'application/json',
      }
      }).then(response => (this.result = response))
    },
    search_date(device_id){
      return axios.get('/date_flask',{
        content: device_id
      },
      {
      headers: {
        'Content-type': 'application/json',
      }
      })
    },
    search_off(){
      return axios.get('/date_flask',{
        content: device_id
      },
      {
      headers: {
        'Content-type': 'application/json',
      }
      })
    }
  }
} 
</script>