// Package controllers stores all the controllers for the Gin router.
package controllers

import (
	"net/http"
	"strconv"

	"TaipeiCityDashboardBE/app/models"
	"TaipeiCityDashboardBE/app/util"

	"github.com/gin-gonic/gin"
)

/*
GetComponentChartData retrieves the chart data for a component.
/api/v1/components/:id/chart

header: time_from, time_to (optional)
*/
func GetComponentChartData(c *gin.Context) {
	// 1. Get the component id from the URL
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "Invalid component ID"})
		return
	}

	// 2. Get the chart data query and chart data type from the database
	queryType, queryString, err := models.GetComponentChartDataQuery(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if (queryString == "") || (queryType == "") {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "No chart data available"})
		return
	}

	timeFrom, timeTo := util.GetTime(c)

	// 3. Get and parse the chart data based on chart data type
	if queryType == "two_d" {
		chartData, err := models.GetTwoDimensionalData(&queryString, timeFrom, timeTo)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "success", "data": chartData})
	} else if queryType == "three_d" || queryType == "percent" {
		chartData, categories, err := models.GetThreeDimensionalData(&queryString, timeFrom, timeTo)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "success", "data": chartData, "categories": categories})
	} else if queryType == "time" {
		chartData, err := models.GetTimeSeriesData(&queryString, timeFrom, timeTo)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "success", "data": chartData})
	} else if queryType == "map_legend" {
		chartData, err := models.GetMapLegendData(&queryString, timeFrom, timeTo)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "success", "data": chartData})
	}
}

/*
GetComponentHistoryData retrieves the history data for a component.
/api/v1/components/:id/history

header: time_from, time_to (mandatory)
timesteps are automatically determined based on the time range:
  - Within 24hrs: hour
  - Within 1 month: day
  - Within 3 months: week
  - Within 2 years: month
  - More than 2 years: year
*/
func GetComponentHistoryData(c *gin.Context) {
	// 1. Get the component id from the URL
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "Invalid component ID"})
		return
	}

	timeFrom, timeTo := util.GetTime(c)

	// 2. Get the history data query from the database
	queryHistory, err := models.GetComponentHistoryDataQuery(id, timeFrom, timeTo)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if queryHistory == "" {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "No history data available"})
		return
	}

	// 3. Get and parse the history data
	chartData, err := models.GetTimeSeriesData(&queryHistory, timeFrom, timeTo)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": "success", "data": chartData})
}


func GetRoadData(c *gin.Context) {
	// 1. Get the component id from the URL

	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "Invalid component ID"})
		return
	}

	queryResult, err := models.GetRoadData(id)
	if err != nil{
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if len(queryResult) == 0 || len(queryResult[0].Data) == 0 {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "No Road data available"})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"status": "success", "data": queryResult})
}

func GetNameData(c *gin.Context) {

	queryResult, err := models.GetNameData()
	if err != nil{
		c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
		return
	}
	if len(queryResult) == 0 || len(queryResult[0].Town) == 0 {
		c.JSON(http.StatusNotFound, gin.H{"status": "error", "message": "No Road data available"})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"status": "success", "data": queryResult})
}

// 半成品
// func UpdateData(c *gin.Context) {

// 	id, err := strconv.Atoi(c.Param("id"))
// 	if err != nil {
// 		c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "Invalid component ID"})
// 		return
// 	}
// 	var req models.UpdateDataRequest

// 	switch id {
// 		case 0:
// 			err = c.ShouldBindJSON(&req)
// 			if err != nil {
// 				c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": err.Error()})
// 				return
// 			}
// 			if req == (models.UpdateDataRequest{}) {
// 				// req 為零值
// 				c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "Doesn't catch data"})
// 				return
// 			}
// 			if err := models.UpdateRainfalldata(req); err != nil{
// 				c.JSON(http.StatusInternalServerError, gin.H{"status": "error", "message": err.Error()})
// 				return
// 			}
			
// 		default:
// 			c.JSON(http.StatusBadRequest, gin.H{"status": "error", "message": "Invalid component ID"})
// 			return
// 	}
// 	c.JSON(http.StatusOK, gin.H{"status": "success"})
// }
