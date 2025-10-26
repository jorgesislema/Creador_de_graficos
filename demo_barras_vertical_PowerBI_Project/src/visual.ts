/**
 * Visual personalizado para Power BI - Gráfico de Barras Verticales
 * Generado por Creador de Gráficos  
 * Tipo: barras_vertical
 */

"use strict";

import "./../style/visual.less";
import powerbi from "powerbi-visuals-api";

import VisualConstructorOptions = powerbi.extensibility.visual.VisualConstructorOptions;
import VisualUpdateOptions = powerbi.extensibility.visual.VisualUpdateOptions;
import IVisual = powerbi.extensibility.visual.IVisual;
import DataView = powerbi.DataView;

export class Visual implements IVisual {
    private target: HTMLElement;

    constructor(options: VisualConstructorOptions) {
        this.target = options.element;
        
        // Crear contenedor principal
        this.target.innerHTML = `
            <div class="visual-container">
                <div class="chart-header">
                    <h3 class="chart-title">Gráfico de Barras Verticales</h3>
                    <p class="chart-description">Comparación de categorías con barras verticales</p>
                </div>
                <div id="chartContainer" class="chart-container">
                    <div class="placeholder">
                        <div class="placeholder-icon">📊</div>
                        <h4>Visual barras_vertical listo</h4>
                        <p>Conecta tus datos para visualizar el gráfico</p>
                        <ul class="placeholder-instructions">
                            <li>Arrastra campos a "Category" para el eje X</li>
                            <li>Arrastra campos a "Values" para el eje Y</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    public update(options: VisualUpdateOptions) {
        const dataView: DataView = options.dataViews[0];
        const chartContainer = this.target.querySelector('#chartContainer') as HTMLElement;
        
        if (!chartContainer) return;
        
        if (!dataView || !dataView.categorical) {
            // Mostrar placeholder si no hay datos
            chartContainer.innerHTML = `
                <div class="placeholder">
                    <div class="placeholder-icon">📊</div>
                    <h4>No hay datos disponibles</h4>
                    <p>Conecta campos de datos para generar el gráfico barras_vertical</p>
                </div>
            `;
            return;
        }
        
        const categorical = dataView.categorical;
        const categories = categorical.categories;
        const values = categorical.values;
        
        // Procesar datos
        let chartData = [];
        if (categories && categories[0] && values && values[0]) {
            const categoryData = categories[0];
            const valueData = values[0];
            
            for (let i = 0; i < categoryData.values.length; i++) {
                chartData.push({
                    category: categoryData.values[i],
                    value: valueData.values[i]
                });
            }
        }
        
        // Renderizar gráfico básico
        this.renderChart(chartContainer, chartData, "barras_vertical");
    }
    
    private renderChart(container: HTMLElement, data: any[], chartType: string) {
        let chartHTML = `
            <div class="chart-content">
                <div class="chart-info">
                    <h4>Gráfico ${chartType}</h4>
                    <p>${data.length} elementos de datos</p>
                </div>
                <div class="data-preview">
        `;
        
        // Mostrar muestra de datos
        data.slice(0, 10).forEach((item, index) => {
            const maxValue = Math.max(...data.map(d => d.value || 0));
            const width = maxValue > 0 ? Math.min(100, (item.value / maxValue) * 100) : 0;
            chartHTML += `
                <div class="data-item">
                    <span class="category">${item.category}</span>
                    <span class="value">${item.value}</span>
                    <div class="bar" style="width: ${width}%"></div>
                </div>
            `;
        });
        
        if (data.length > 10) {
            chartHTML += `<p class="more-data">... y ${data.length - 10} elementos más</p>`;
        }
        
        chartHTML += `
                </div>
            </div>
        `;
        
        container.innerHTML = chartHTML;
    }
}