'use client';

import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

interface Planet {
  name: string;
  symbol: string;
  degree: number;
  sign: string;
  house: number;
  aspects: Array<{
    planet: string;
    type: string;
    orb: number;
  }>;
}

interface House {
  number: number;
  degree: number;
  sign: string;
}

interface BirthChartData {
  planets: Planet[];
  houses: House[];
  ascendant: number;
  midheaven: number;
}

interface BirthChartVisualizationProps {
  data: BirthChartData;
  name: string;
  birthDate: string;
  birthTime: string;
  birthPlace: string;
}

const ZODIAC_SIGNS = [
  { name: 'Aries', symbol: '♈', color: '#FF4136' },
  { name: 'Taurus', symbol: '♉', color: '#2ECC40' },
  { name: 'Gemini', symbol: '♊', color: '#FFDC00' },
  { name: 'Cancer', symbol: '♋', color: '#B10DC9' },
  { name: 'Leo', symbol: '♌', color: '#FF851B' },
  { name: 'Virgo', symbol: '♍', color: '#7FDBFF' },
  { name: 'Libra', symbol: '♎', color: '#01FF70' },
  { name: 'Scorpio', symbol: '♏', color: '#F012BE' },
  { name: 'Sagittarius', symbol: '♐', color: '#001F3F' },
  { name: 'Capricorn', symbol: '♑', color: '#39CCCC' },
  { name: 'Aquarius', symbol: '♒', color: '#85144B' },
  { name: 'Pisces', symbol: '♓', color: '#3D9970' },
];

const ASPECT_TYPES = {
  conjunction: { symbol: '☌', color: '#FFD700', description: 'Planets are very close together (0°)' },
  opposition: { symbol: '☍', color: '#FF4136', description: 'Planets are opposite each other (180°)' },
  trine: { symbol: '△', color: '#2ECC40', description: 'Planets are 120° apart' },
  square: { symbol: '□', color: '#FF851B', description: 'Planets are 90° apart' },
  sextile: { symbol: '⚹', color: '#7FDBFF', description: 'Planets are 60° apart' },
};

export default function BirthChartVisualization({
  data,
  name,
  birthDate,
  birthTime,
  birthPlace,
}: BirthChartVisualizationProps) {
  const chartRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!chartRef.current || !data) return;

    const width = 600;
    const height = 600;
    const radius = Math.min(width, height) / 2 - 40;

    // Clear previous chart
    d3.select(chartRef.current).selectAll('*').remove();

    const svg = d3.select(chartRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);

    // Draw zodiac wheel
    const zodiacWheel = svg.append('g').attr('class', 'zodiac-wheel');

    // Draw houses
    const houseArc = d3.arc()
      .innerRadius(radius * 0.6)
      .outerRadius(radius);

    data.houses.forEach((house, i) => {
      const startAngle = ((house.degree - data.ascendant + 360) % 360) * (Math.PI / 180);
      const endAngle = ((data.houses[(i + 1) % 12].degree - data.ascendant + 360) % 360) * (Math.PI / 180);

      zodiacWheel.append('path')
        .attr('d', houseArc({
          startAngle,
          endAngle,
        } as any))
        .attr('fill', 'none')
        .attr('stroke', '#666')
        .attr('stroke-width', 1);

      // Add house numbers
      const midAngle = (startAngle + endAngle) / 2;
      const [x, y] = d3.pointRadial(midAngle, radius * 0.8);
      
      zodiacWheel.append('text')
        .attr('x', x)
        .attr('y', y)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .text(house.number.toString());
    });

    // Draw zodiac signs
    const signArc = d3.arc()
      .innerRadius(radius * 0.9)
      .outerRadius(radius);

    ZODIAC_SIGNS.forEach((sign, i) => {
      const startAngle = (i * 30 - data.ascendant + 360) % 360 * (Math.PI / 180);
      const endAngle = ((i + 1) * 30 - data.ascendant + 360) % 360 * (Math.PI / 180);

      zodiacWheel.append('path')
        .attr('d', signArc({
          startAngle,
          endAngle,
        } as any))
        .attr('fill', sign.color)
        .attr('opacity', 0.2);

      const midAngle = (startAngle + endAngle) / 2;
      const [x, y] = d3.pointRadial(midAngle, radius * 0.95);

      zodiacWheel.append('text')
        .attr('x', x)
        .attr('y', y)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .text(sign.symbol);
    });

    // Draw planets
    data.planets.forEach((planet) => {
      const angle = (planet.degree - data.ascendant + 360) % 360 * (Math.PI / 180);
      const [x, y] = d3.pointRadial(angle, radius * 0.7);

      zodiacWheel.append('text')
        .attr('x', x)
        .attr('y', y)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .attr('class', 'planet')
        .text(planet.symbol);
    });

    // Draw aspects
    const aspectGroup = svg.append('g').attr('class', 'aspects');

    data.planets.forEach((planet1, i) => {
      planet1.aspects.forEach((aspect) => {
        const planet2 = data.planets.find(p => p.name === aspect.planet);
        if (!planet2 || i >= data.planets.indexOf(planet2)) return;

        const angle1 = (planet1.degree - data.ascendant + 360) % 360 * (Math.PI / 180);
        const angle2 = (planet2.degree - data.ascendant + 360) % 360 * (Math.PI / 180);
        const [x1, y1] = d3.pointRadial(angle1, radius * 0.5);
        const [x2, y2] = d3.pointRadial(angle2, radius * 0.5);

        aspectGroup.append('line')
          .attr('x1', x1)
          .attr('y1', y1)
          .attr('x2', x2)
          .attr('y2', y2)
          .attr('stroke', ASPECT_TYPES[aspect.type as keyof typeof ASPECT_TYPES].color)
          .attr('stroke-width', 1)
          .attr('opacity', 0.5);
      });
    });
  }, [data]);

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>{name}'s Birth Chart</CardTitle>
        <CardDescription>
          Born on {birthDate} at {birthTime} in {birthPlace}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="chart">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="chart">Chart</TabsTrigger>
            <TabsTrigger value="details">Details</TabsTrigger>
          </TabsList>
          <TabsContent value="chart" className="flex justify-center">
            <svg ref={chartRef} />
          </TabsContent>
          <TabsContent value="details" className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">Planetary Positions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.planets.map((planet) => (
                  <div key={planet.name} className="flex items-center space-x-2">
                    <span className="text-xl">{planet.symbol}</span>
                    <span>{planet.name}</span>
                    <Badge variant="outline">
                      {planet.degree.toFixed(2)}° {planet.sign}
                    </Badge>
                    <Badge>House {planet.house}</Badge>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Aspects</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.planets.map((planet) =>
                  planet.aspects.map((aspect, i) => (
                    <TooltipProvider key={`${planet.name}-${aspect.planet}-${i}`}>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <div className="flex items-center space-x-2 cursor-help">
                            <span>{planet.symbol}</span>
                            <span className="text-xl" style={{ color: ASPECT_TYPES[aspect.type as keyof typeof ASPECT_TYPES].color }}>
                              {ASPECT_TYPES[aspect.type as keyof typeof ASPECT_TYPES].symbol}
                            </span>
                            <span>{data.planets.find(p => p.name === aspect.planet)?.symbol}</span>
                            <Badge variant="outline">{aspect.orb.toFixed(2)}°</Badge>
                          </div>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>{ASPECT_TYPES[aspect.type as keyof typeof ASPECT_TYPES].description}</p>
                          <p>Orb: {aspect.orb.toFixed(2)}°</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  ))
                )}
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}