<!-- Developed By Taipei Urban Intelligence Center 2023-2024 -->
<!-- 
Lead Developer:  Igor Ho (Full Stack Engineer)
Data Pipelines:  Iima Yu (Data Scientist)
Design and UX: Roy Lin (Fmr. Consultant), Chu Chen (Researcher)
Systems: Ann Shih (Systems Engineer)
Testing: Jack Huang (Data Scientist), Ian Huang (Data Analysis Intern) 
-->
<!-- Department of Information Technology, Taipei City Government -->

<!-- Map charts will be hidden in mobile mode and be replaced with the mobileLayers dialog -->

<script setup>
import axios from "axios";
import { ref, watch, onMounted } from "vue";
import { useContentStore } from "../store/contentStore";
import { useDialogStore } from "../store/dialogStore";
import { useMapStore } from "../store/mapStore";

import MapContainer from "../components/map/MapContainer.vue";
import MoreInfo from "../components/dialogs/MoreInfo.vue";
import ReportIssue from "../components/dialogs/ReportIssue.vue";

const contentStore = useContentStore();
const dialogStore = useDialogStore();
// const mapStore = useMapStore();

// Data for dropdowns
const selectedTown = ref("");
const selectedRoad = ref("");
const towns = ref([]);
const roads = ref([]);

// Function to fetch towns from the first API
async function fetchTowns() {
	try {
		const response = await axios.get(
			"http://localhost:8088/api/v1/component/road"
		);
		const townsData = response.data.data.map((item) => item.town);
		towns.value = townsData;
	} catch (error) {
		console.error("Error fetching towns:", error);
	}
}

async function updateRoads(selectedTownIndex) {
	console.log(selectedTownIndex);
	if (selectedTownIndex !== null && selectedTownIndex !== undefined) {
		const selectedTownId = selectedTownIndex; // 假設 id 就是索引本身
		try {
			const response = await axios.get(
				"http://localhost:8088/api/v1/component/road/${selectedTownId}"
			);
			const placeNames = response.data.data[0].data.map(
				(item) => item.place_name
			);
			roads.value = placeNames;
		} catch (error) {
			console.error("Error fetching roads:", error);
		}
	} else {
		roads.value = [];
	}
}

// 渲染時就呼叫第一次api
onMounted(fetchTowns);

function handleOpenSettings() {
	contentStore.editDashboard = JSON.parse(
		JSON.stringify(contentStore.currentDashboard)
	);
	dialogStore.addEdit = "edit";
	dialogStore.showDialog("addEditDashboards");
}

function handleSubmit() {
	//處理資料送回後端的api
	const selectedTownValue = selectedTown.value;
	const selectedRoadValue = selectedRoad.value;
	const suggestionText = document.querySelector(".input-wrapper input").value;

	// 发送数据给后端
	axios
		.post("your_backend_api_url", {
			town: selectedTownValue,
			road: selectedRoadValue,
			suggestion: suggestionText,
		})
		.then((response) => {
			console.log("提交成功！", response.data);
			// 可以在这里执行其他操作，例如显示成功消息等
		})
		.catch((error) => {
			console.error("提交失败！", error);
			// 可以在这里执行其他操作，例如显示错误消息等
		});
}
</script>

<template>
	<div class="questionboard">
		<div class="question-select">
			<h2>請選擇地區</h2>
			<select
				v-model="selectedTown"
				@change="updateRoads($event.target.selectedIndex)"
			>
				<option v-if="!selectedTown" disabled value="">請選擇</option>
				<option v-for="town in towns" :value="town">{{ town }}</option>
			</select>
			<select v-model="selectedRoad">
				<option value="">請選擇</option>
				<option v-for="road in roads" :value="road">
					{{ road }}
				</option>
			</select>
			<div class="input-wrapper">
				<input type="text" placeholder="請輸入問題..." />
			</div>
			<button @click="handleSubmit">提交</button>
		</div>
		<MapContainer />
		<MoreInfo />
		<ReportIssue />
	</div>
</template>

<style scoped lang="scss">
.questionboard {
	height: calc(100vh - 127px);
	height: calc(var(--vh) * 100 - 127px);
	display: flex;
	margin: var(--font-m) var(--font-m);

	&-charts {
		width: 360px;
		max-height: 100%;
		height: fit-content;
		display: grid;
		row-gap: var(--font-m);
		margin-right: var(--font-s);
		border-radius: 5px;
		overflow-y: scroll;

		@media (min-width: 1000px) {
			width: 370px;
		}

		@media (min-width: 2000px) {
			width: 400px;
		}

		&-nodashboard {
			width: 360px;
			height: calc(100vh - 127px);
			height: calc(var(--vh) * 100 - 127px);
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			margin-right: var(--font-s);

			@media (min-width: 1000px) {
				width: 370px;
			}

			@media (min-width: 2000px) {
				width: 400px;
			}

			span {
				margin-bottom: var(--font-ms);
				font-family: var(--font-icon);
				font-size: 2rem;
			}

			button {
				color: var(--color-highlight);
			}

			div {
				width: 2rem;
				height: 2rem;
				border-radius: 50%;
				border: solid 4px var(--color-border);
				border-top: solid 4px var(--color-highlight);
				animation: spin 0.7s ease-in-out infinite;
			}
		}
	}
}

.input-wrapper {
	width: 100%;
	max-width: 300px;
}

input {
	margin-top: 10px;
	width: 200px;
	height: 400px;
	padding: 8px;
	font-size: 16px;
	border: 1px solid #ccc;
	border-radius: 5px;
	text-align: left;
	resize: vertical;
	overflow-y: auto;
	word-wrap: break-word;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}
</style>
