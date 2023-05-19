<template>
  <div>
    <p>COVID death prediction ML model UI</p>
    <div>
      <Modal v-model:visible="isChartModalVisible" title="График предсказаний">
        <Line :data="this.chartData"> </Line>
      </Modal>
      <div
        style="
          display: flex;
          flex-direction: row;
          justify-content: space-between;
        "
      >
        <div
          style="
            display: flex;
            justify-content: flex-start;
            flex-direction: row;
            align-items: center;
          "
        >
          <button v-on:click="onClearInputClick" style="margin-right: 1%">
            Очистить поля
          </button>
          <button v-on:click="onSavePointClick" style="margin-right: 1%">
            Добавить точку
          </button>
          <button
            v-on:click="onPreviousPointClick"
            :disabled="currentPoint == 0"
            style="margin-right: 1%"
          >
            Предыдущая точка
          </button>
          <button
            v-on:click="onNextPointClick"
            :disabled="
              this.history.length == 0 ||
              this.currentPoint + 1 >= this.history.length
            "
            style="margin-right: 1%"
          >
            Следующая точка
          </button>
          <button v-on:click="onClearHistoryClick" style="margin-right: 1%">
            Удалить точки
          </button>
          <button v-on:click="onButtonClick" style="margin-right: 1%">
            Сделать предсказание
          </button>
          <button
            v-on:click="onPredictManyClick"
            :disabled="this.history.length == 0"
            style="margin-right: 1%"
          >
            Предсказать по точкам
          </button>
          <p>
            {{ currentPointCaption }}
          </p>
        </div>
        <div
          style="
            display: flex;
            justify-content: flex-start;
            align-items: center;
            flex-direction: row;
          "
        >
          <p>Вроятность смерти: {{ prediction }}</p>
        </div>
      </div>
    </div>
    <div class="input-container">
      <div class="input-layout-column">
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Пол:</span>
          <select v-model="sex">
            <option disabled value="">Выберите пол</option>
            <option v-bind:value="false">Мужской</option>
            <option v-bind:value="true">Женский</option>
          </select>
          <div v-show="sex">
            <label for="checkbox" style="padding-right: 15px"> Беременна</label>
            <input
              type="checkbox"
              id="checkbox-pregnant"
              v-model="isPregnant"
            />
          </div>
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Вес:</span>
          <input v-model="weight" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Температура max:</span>
          <input v-model="maxTemp" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Максимальная степень ДН:</span>
          <select v-model="maxDNSeverityCategory">
            <option disabled value="">Выберите степень</option>
            <option>0</option>
            <option>1</option>
            <option>2</option>
            <option>3</option>
          </select>
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px">Курит</label>
          <input type="checkbox" id="checkbox-smoking" v-model="isSmoking" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px">Рак</label>
          <input type="checkbox" id="checkbox-cancer" v-model="hasCancer" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px">ВИЧ-инфекция</label>
          <input type="checkbox" id="checkbox-hiv" v-model="hasHIV" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px">Пневмония</label>
          <input type="checkbox" id="checkbox-pneumo" v-model="hasPneumo" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Бронхиальная астма</label
          >
          <input type="checkbox" id="checkbox-asthma" v-model="hasAsthma" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px">Диабет</label>
          <input type="checkbox" id="checkbox-diabetes" v-model="hasDiabetes" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px">Ожирение</label>
          <input type="checkbox" id="checkbox-obesity" v-model="hasObesity" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Вакцинирован от COVID-19</label
          >
          <input type="checkbox" id="checkbox-covidvac" v-model="covidVac" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Вакцинирован от пневмококковой инфекции</label
          >
          <input
            type="checkbox"
            id="checkbox-pneumococcusvac"
            v-model="pneumococcusVac"
          />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Общий белок max:</span>
          <input
            v-model="maxCommonProtein"
            :placeholder="numberInputPlaceholder"
          />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Глюкоза max:</span>
          <input v-model="maxGlucose" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Аланинаминотрансфераза max:</span>
          <input v-model="maxALT" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Аспартатаминотрансфераза max:</span>
          <input v-model="maxAST" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Билирубин max:</span>
          <input v-model="maxBilirubin" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">МНО max:</span>
          <input v-model="maxMNO" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">МНО min:</span>
          <input v-model="minMNO" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Протромбиновый индекс min:</span>
          <input
            v-model="minProtrombIndex"
            :placeholder="numberInputPlaceholder"
          />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Фибриноген max:</span>
          <input
            v-model="maxFibrinogen"
            :placeholder="numberInputPlaceholder"
          />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Факт госпитализации в отделение реанимации</label
          >
          <input
            type="checkbox"
            id="checkbox-resus"
            v-model="wasInResuscitation"
          />
        </div>
      </div>
      <div class="input-layout-column">
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Возраст:</span>
          <input v-model="age" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Частода дыхания max:</span>
          <input v-model="maxBP" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Сатурация O2 min:</span>
          <input
            v-model="minSaturation"
            :placeholder="numberInputPlaceholder"
          />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px"
            >Cтепень поражения лёгких по КТ :</span
          >
          <select v-model="maxKT">
            <option disabled value="">Выберите степень</option>
            <option>0</option>
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
          </select>
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px">Работает</label>
          <input type="checkbox" id="checkbox-employed" v-model="isEmployed" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Ишемическая болезнь сердца</label
          >
          <input type="checkbox" id="checkbox-ibs" v-model="hasIBS" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Инфаркт миокарда</label
          >
          <input
            type="checkbox"
            id="checkbox-myocard"
            v-model="hasMyocardInfarct"
          />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Острое нарушение мозгового кровообращения</label
          >
          <input type="checkbox" id="checkbox-onmk" v-model="hasONMK" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Артериальная гипертония</label
          >
          <input
            type="checkbox"
            id="checkbox-hypertonia"
            v-model="hasHypertonia"
          />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Хроническая обструктивная болезнь легких</label
          >
          <input type="checkbox" id="checkbox-hobl" v-model="hasHOBL" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Почечная недостаточность</label
          >
          <input type="checkbox" id="checkbox-hpn" v-model="hasHPN" />
        </div>
        <div style="padding-top: 15px">
          <label for="checkbox" style="padding-right: 15px"
            >Вакцинирован от гриппа</label
          >
          <input type="checkbox" id="checkbox-fluvac" v-model="fluVac" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Лимфоциты (абс) min:</span>
          <input v-model="minAbsLymph" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Лейкоциты (абс) max:</span>
          <input v-model="maxAbsLeic" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Гемоглобин min:</span>
          <input
            v-model="minHemoglobin"
            :placeholder="numberInputPlaceholder"
          />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Тромбоциты (абс) max:</span>
          <input v-model="maxPlt" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">СОЭ max:</span>
          <input v-model="maxESR" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">С-реактивный белок max:</span>
          <input v-model="maxCProtein" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Ферритин max:</span>
          <input v-model="maxFerritin" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Д-димер max:</span>
          <input v-model="maxDDimer" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Мочевина max:</span>
          <input v-model="maxUrea" :placeholder="numberInputPlaceholder" />
        </div>
        <div style="padding-top: 15px">
          <span style="padding-right: 15px">Креатинин max:</span>
          <input
            v-model="maxCreatinine"
            :placeholder="numberInputPlaceholder"
          />
        </div>
        <div style="padding-top: 15px">
          <div v-show="wasInResuscitation">
            <label for="checkbox" style="padding-right: 15px">ИВЛ</label>
            <input type="checkbox" id="checkbox-ivl" v-model="wasOnIVL" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as tf from "@tensorflow/tfjs";
import { Modal } from "usemodal-vue3";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";
import { Line } from "vue-chartjs";
ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  Title,
  Tooltip,
  Legend,
  PointElement
);

export default {
  name: "MainWindow",
  components: { Modal, Line },
  data() {
    return {
      history: [],
      fieldsNames: [
        "sex",
        "age",
        "weight",
        "isSmoking",
        "isPregnant",
        "minAbsLymph",
        "maxAbsLeic",
        "maxPlt",
        "maxESR",
        "maxCProtein",
        "maxFerritin",
        "maxDDimer",
        "maxUrea",
        "maxCommonProtein",
        "maxGlucose",
        "maxALT",
        "maxAST",
        "maxBilirubin",
        "maxMNO",
        "minMNO",
        "minProtrombIndex",
        "maxFibrinogen",
        "maxCreatinine",
        "minHemoglobin",
        "maxTemp",
        "minSaturation",
        "maxBP",
        "isEmployed",
        "hasIBS",
        "hasMyocardInfarct",
        "hasONMK",
        "hasHypertonia",
        "hasHOBL",
        "hasDiabetes",
        "hasObesity",
        "hasHPN",
        "hasCancer",
        "hasHIV",
        "hasPneumo",
        "hasAsthma",
        "covidVac",
        "fluVac",
        "pneumococcusVac",
        "wasInResuscitation",
        "wasOnIVL",
        "maxDNSeverityCategory",
        "maxKT",
        "prediction",
      ],
      currentPoint: 0,
      currentPointCaption: "Точка 1",
      numberInputPlaceholder: "Введите число",
      sex: "",
      age: null,
      weight: null,
      isSmoking: false,
      isPregnant: false,
      maxDNSeverityCategory: "",
      isEmployed: false,
      hasIBS: false,
      hasMyocardInfarct: false,
      hasONMK: false,
      hasHypertonia: false,
      hasHOBL: false,
      hasDiabetes: false,
      hasObesity: false,
      hasHPN: false,
      hasCancer: false,
      hasHIV: false,
      hasPneumo: false,
      hasAsthma: false,
      covidVac: false,
      fluVac: false,
      pneumococcusVac: false,
      minAbsLymph: null,
      maxAbsLeic: null,
      maxPlt: null,
      maxESR: null,
      maxCProtein: null,
      maxFerritin: null,
      maxDDimer: null,
      maxUrea: null,
      maxCommonProtein: null,
      maxGlucose: null,
      maxALT: null,
      maxAST: null,
      maxBilirubin: null,
      maxMNO: null,
      minMNO: null,
      minProtrombIndex: null,
      maxFibrinogen: null,
      maxCreatinine: null,
      minHemoglobin: null,
      maxTemp: null,
      minSaturation: null,
      maxBP: null,
      maxKT: "",
      wasOnIVL: false,
      wasInResuscitation: false,
      prediction: "0.0000%",
      isChartModalVisible: false,
      chartData: {
        labels: ["0"],
        datasets: [
          {
            label: "Вероятность",
            backgroundColor: "#f87979",
            data: [],
          },
        ],
      },
    };
  },
  methods: {
    async onButtonClick() {
      this.prediction = await this.getPrediction();
    },

    async predictDataByHistory() {
      if (this.currentPoint === this.history.length) {
        this.writeHistory();
      } else {
        this.history[this.currentPoint] = this.saveHistory();
      }
      const model = await tf.loadLayersModel("http://localhost:9731/get_model");
      const columnsToGet = this.fieldsNames.filter(
        (name) =>
          !["maxDNSeverityCategory", "maxKT", "prediction"].includes(name)
      );
      let dataArray = [];
      let dnCategoryArray = [];
      let ktCategoryArray = [];
      this.history.forEach((item) => {
        let dataObject = [];
        columnsToGet.forEach((name) => {
          if (name === "isEmployed") {
            dataObject.push(!item[name]);
          } else {
            dataObject.push(item[name]);
          }
        });
        const castedData = dataObject.map((item) => this.castValue(item));
        dataArray.push(tf.tensor([castedData]));
        dnCategoryArray.push(this.encodeData(item["maxDNSeverityCategory"], 3));
        ktCategoryArray.push(this.encodeData(item["maxKT"], 5));
      });
      //dataArray.push(tf.tensor([this.getDataFormData()]));
      const concatData = tf.concat1d(dataArray, 0);
      const concatDN = tf.concat1d(dnCategoryArray, 1);
      const concatKT = tf.concat1d(ktCategoryArray, 1);
      const pred = model.predict([concatData, concatDN, concatKT]);
      const predictionsArray = pred.dataSync().map((item) => item * 100);
      this.chartData = {
        labels: [...Array(predictionsArray.length).keys()],
        datasets: [
          {
            label: "Вероятность",
            backgroundColor: "#f87979",
            data: predictionsArray,
          },
        ],
      };
    },

    async getPrediction() {
      const model = await tf.loadLayersModel("http://localhost:9731/get_model");
      const castedData = this.getDataFormData();
      const tensorNumeric = tf.tensor([castedData]);
      const tensorDN = this.encodeData(this.maxDNSeverityCategory, 3);
      const tensorKT = this.encodeData(this.maxKT, 5);
      const pred = model.predict([tensorNumeric, tensorDN, tensorKT]);
      return pred.dataSync()[0];
    },

    getDataFormData() {
      const columnsToGet = this.fieldsNames.filter(
        (name) =>
          !["maxDNSeverityCategory", "maxKT", "prediction"].includes(name)
      );
      let data = [];
      columnsToGet.forEach((name) => {
          if (name === "isEmployed") {
            data.push(!this[name]);
          } else {
            data.push(this[name]);
          }
        });
      return data.map((item) => this.castValue(item));
    },

    castValue(value) {
      let val = value;
      if (typeof value === "string") {
        val = value.replace(/,/g, ".");
      }
      return Number(val);
    },

    encodeData(value, numClasses) {
      return tf.oneHot(tf.tensor1d([value], "int32"), numClasses);
    },

    onSavePointClick() {
      if (
        this.history.length != 0 &&
        this.currentPoint != this.history.length
      ) {
        this.history[this.currentPoint] = this.saveHistory();
      } else {
        this.writeHistory();
      }
      this.currentPoint = this.history.length;
      this.prediction = "0.0000%";
    },

    onClearInputClick() {
      this.fieldsNames.forEach((item) => {
        this[item] = "";
      });
      this.prediction = "0.0000%";
    },

    onPreviousPointClick() {
      if (this.currentPoint === this.history.length) {
        this.writeHistory();
      } else {
        this.history[this.currentPoint] = this.saveHistory();
      }
      this.currentPoint--;
      this.loadHistory();
    },

    onNextPointClick() {
      this.history[this.currentPoint] = this.saveHistory();
      this.currentPoint++;
      this.loadHistory();
    },

    onClearHistoryClick() {
      this.history = [];
      this.currentPoint = 0;
      this.currentPointCaption = "Точка 1";
    },

    onPredictManyClick() {
      this.isChartModalVisible = true;
      this.predictDataByHistory();
    },

    saveHistory() {
      let historyObj = {};
      this.fieldsNames.forEach((fieldName) => {
        historyObj[fieldName] = this[fieldName];
      });
      return historyObj;
    },

    writeHistory() {
      const historyObj = this.saveHistory();
      this.history.push(historyObj);
      console.log(this.history);
    },

    loadHistory() {
      const historyObj = this.history[this.currentPoint];
      this.fieldsNames.forEach((fieldName) => {
        this[fieldName] = historyObj[fieldName];
      });
    },
  },
  watch: {
    maxDNSeverityCategory() {
      console.log(this.maxDNSeverityCategory);
    },

    currentPoint() {
      const historyCount = this.history.length;
      if (historyCount != 0) {
        this.currentPointCaption =
          this.currentPoint >= historyCount
            ? `Точка ${this.currentPoint + 1}`
            : `Точка ${this.currentPoint + 1} из ${historyCount}`;
      } else {
        this.currentPointCaption = "Точка 1";
      }
    },

    getChartData() {
      const pointsNumber = this.chartData.length;
      return {
        labels: [...Array(pointsNumber).keys()],
        datasets: [
          {
            label: "prediction",
            data: this.chartData,
          },
        ],
      };
    },
  },
  // mounted() {

  // }
};
</script>

<style lang="css">
.input-container {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  height: 745px;
  overflow-y: scroll;
}
.input-layout-column {
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: space-evenly;
  padding-top: 2%;
  align-items: flex-end;
}
</style>
