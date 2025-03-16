'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/services/api';
import BirthChartVisualization from '@/components/BirthChartVisualization';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Share2, Download, ArrowLeft } from 'lucide-react';

interface BirthChartData {
  id: string;
  name: string;
  birthDate: string;
  birthTime: string;
  birthPlace: string;
  chartData: {
    planets: Array<{
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
    }>;
    houses: Array<{
      number: number;
      degree: number;
      sign: string;
    }>;
    ascendant: number;
    midheaven: number;
  };
}

export default function BirthChartResultPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [chartData, setChartData] = useState<BirthChartData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login?redirect=/birth-chart/' + params.id);
      return;
    }

    const fetchChartData = async () => {
      try {
        const response = await api.getBirthChart(params.id);
        setChartData(response.data);
      } catch (err) {
        setError('Failed to load birth chart data. Please try again.');
        console.error('Error fetching birth chart:', err);
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      fetchChartData();
    }
  }, [params.id, user, authLoading, router]);

  const handleShare = async () => {
    try {
      await navigator.share({
        title: `${chartData?.name}'s Birth Chart - MyDivinations`,
        text: `Check out ${chartData?.name}'s astrological birth chart on MyDivinations!`,
        url: window.location.href,
      });
    } catch (err) {
      console.error('Error sharing:', err);
    }
  };

  const handleDownload = async () => {
    try {
      const svg = document.querySelector('svg');
      if (!svg) return;

      const svgData = new XMLSerializer().serializeToString(svg);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();

      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx?.drawImage(img, 0, 0);
        
        const link = document.createElement('a');
        link.download = `${chartData?.name}-birth-chart.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
      };

      img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    } catch (err) {
      console.error('Error downloading chart:', err);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="container mx-auto py-8 flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error || !chartData) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Card className="max-w-lg mx-auto p-6 text-center">
          <h2 className="text-2xl font-bold mb-4">Error</h2>
          <p className="text-muted-foreground mb-6">{error || 'Failed to load birth chart data.'}</p>
          <Button onClick={() => router.push('/birth-chart')}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Create New Chart
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="flex items-center justify-between">
          <Button
            variant="outline"
            onClick={() => router.push('/birth-chart')}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
          <div className="space-x-2">
            <Button variant="outline" onClick={handleShare}>
              <Share2 className="mr-2 h-4 w-4" />
              Share
            </Button>
            <Button variant="outline" onClick={handleDownload}>
              <Download className="mr-2 h-4 w-4" />
              Download
            </Button>
          </div>
        </div>

        <BirthChartVisualization
          data={chartData.chartData}
          name={chartData.name}
          birthDate={chartData.birthDate}
          birthTime={chartData.birthTime}
          birthPlace={chartData.birthPlace}
        />

        <div className="text-center text-sm text-muted-foreground">
          <p>
            This birth chart was calculated using precise astronomical data and represents the exact positions
            of celestial bodies at the time and location of birth.
          </p>
        </div>
      </div>
    </div>
  );
}