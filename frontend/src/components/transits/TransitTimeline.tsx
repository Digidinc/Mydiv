'use client';

import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { format, addDays, subDays, differenceInDays } from 'date-fns';
import { motion } from 'framer-motion';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Transit, TransitPeriod } from '@/types/transits';

interface TransitTimelineProps {
  transitPeriod: TransitPeriod;
  onTransitClick: (transit: Transit) => void;
}

const COLORS = {
  harmonious: '#22c55e',
  challenging: '#ef4444',
  neutral: '#64748b',
  mixed: '#eab308',
};

const ZOOM_LEVELS = [7, 14, 30, 90, 180, 365];

export default function TransitTimeline({ transitPeriod, onTransitClick }: TransitTimelineProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [zoomLevel, setZoomLevel] = useState(2); // Index in ZOOM_LEVELS
  const [centerDate, setCenterDate] = useState(new Date());
  const [hoveredTransit, setHoveredTransit] = useState<Transit | null>(null);

  useEffect(() => {
    if (!svgRef.current || !transitPeriod) return;

    const margin = { top: 20, right: 30, bottom: 30, left: 50 };
    const width = svgRef.current.clientWidth - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Clear previous chart
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Calculate date range
    const days = ZOOM_LEVELS[zoomLevel];
    const startDate = subDays(centerDate, days / 2);
    const endDate = addDays(centerDate, days / 2);

    // Create scales
    const xScale = d3.scaleTime()
      .domain([startDate, endDate])
      .range([0, width]);

    const yScale = d3.scaleLinear()
      .domain([0, 10]) // Influence strength range
      .range([height, 0]);

    // Create axes
    const xAxis = d3.axisBottom(xScale)
      .ticks(width > 600 ? 10 : 5)
      .tickFormat((d) => format(d as Date, 'd MMM'));

    const yAxis = d3.axisLeft(yScale)
      .ticks(5)
      .tickFormat((d) => `${d}`);

    // Add axes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(xAxis);

    svg.append('g')
      .call(yAxis);

    // Add grid lines
    svg.append('g')
      .attr('class', 'grid')
      .attr('opacity', 0.1)
      .call(d3.axisLeft(yScale)
        .ticks(5)
        .tickSize(-width)
        .tickFormat(() => '')
      );

    // Filter transits within the date range
    const visibleTransits = transitPeriod.transits.filter(transit => {
      const { start, end } = transit.influence.duration;
      return start <= endDate && end >= startDate;
    });

    // Draw transit paths
    visibleTransits.forEach(transit => {
      const { start, peak, end } = transit.influence.duration;
      const strength = transit.influence.strength;

      const points = [
        [start, 0],
        [peak, strength],
        [end, 0],
      ].map(([date, str]) => [
        xScale(date),
        yScale(str),
      ]);

      const line = d3.line()(points as [number, number][]);

      svg.append('path')
        .attr('d', line)
        .attr('fill', 'none')
        .attr('stroke', COLORS[transit.influence.nature])
        .attr('stroke-width', 2)
        .attr('opacity', 0.7)
        .style('cursor', 'pointer')
        .on('mouseover', () => setHoveredTransit(transit))
        .on('mouseout', () => setHoveredTransit(null))
        .on('click', () => onTransitClick(transit));
    });

    // Add significant dates
    transitPeriod.summary.significantDates
      .filter(date => date.date >= startDate && date.date <= endDate)
      .forEach(({ date, importance }) => {
        svg.append('circle')
          .attr('cx', xScale(date))
          .attr('cy', yScale(importance))
          .attr('r', 4)
          .attr('fill', '#fff')
          .attr('stroke', '#000')
          .attr('stroke-width', 2);
      });
  }, [transitPeriod, zoomLevel, centerDate, onTransitClick]);

  const handleZoomIn = () => {
    if (zoomLevel > 0) {
      setZoomLevel(zoomLevel - 1);
    }
  };

  const handleZoomOut = () => {
    if (zoomLevel < ZOOM_LEVELS.length - 1) {
      setZoomLevel(zoomLevel + 1);
    }
  };

  const handlePan = (direction: 'left' | 'right') => {
    const days = ZOOM_LEVELS[zoomLevel] / 4;
    setCenterDate(direction === 'left' 
      ? subDays(centerDate, days)
      : addDays(centerDate, days)
    );
  };

  return (
    <Card className="p-4">
      <div className="flex items-center justify-between mb-4">
        <div className="space-x-2">
          <Button
            variant="outline"
            size="icon"
            onClick={() => handlePan('left')}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            onClick={() => handlePan('right')}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="icon"
            onClick={handleZoomIn}
            disabled={zoomLevel === 0}
          >
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            onClick={handleZoomOut}
            disabled={zoomLevel === ZOOM_LEVELS.length - 1}
          >
            <ZoomOut className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="relative">
        <svg ref={svgRef} className="w-full" />
        
        {hoveredTransit && (
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <div className="absolute top-0 left-0 pointer-events-none">
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-card p-4 rounded-lg shadow-lg"
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span>{hoveredTransit.transitingPlanet.symbol}</span>
                      <span>{hoveredTransit.aspect.type}</span>
                      <span>{hoveredTransit.natalPlanet.symbol}</span>
                    </div>
                    <div className="text-sm">
                      <p>Strength: {hoveredTransit.influence.strength}</p>
                      <p>Nature: {hoveredTransit.influence.nature}</p>
                      {hoveredTransit.aspect.exactDate && (
                        <p>Exact: {format(hoveredTransit.aspect.exactDate, 'PP')}</p>
                      )}
                    </div>
                  </motion.div>
                </div>
              </TooltipTrigger>
            </Tooltip>
          </TooltipProvider>
        )}
      </div>

      <div className="flex justify-between text-sm text-muted-foreground mt-4">
        <div className="flex items-center gap-4">
          {Object.entries(COLORS).map(([nature, color]) => (
            <div key={nature} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: color }}
              />
              <span className="capitalize">{nature}</span>
            </div>
          ))}
        </div>
        <div>
          Showing {ZOOM_LEVELS[zoomLevel]} days
        </div>
      </div>
    </Card>
  );
}