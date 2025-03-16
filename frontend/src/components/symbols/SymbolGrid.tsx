'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Symbol, SymbolCategory } from '@/types/symbols';
import SymbolCard from './SymbolCard';

interface SymbolGridProps {
  symbols: Symbol[];
  onSymbolInteraction: (symbolId: string, type: 'study' | 'meditation' | 'practice' | 'insight') => void;
}

const CATEGORIES: SymbolCategory[] = [
  'zodiac',
  'planet',
  'house',
  'aspect',
  'node',
  'element',
  'fixed_star',
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

export default function SymbolGrid({ symbols, onSymbolInteraction }: SymbolGridProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<SymbolCategory | 'all'>('all');
  const [sortBy, setSortBy] = useState<'name' | 'progress' | 'recent'>('progress');

  const filteredSymbols = symbols.filter(symbol => {
    const matchesSearch = symbol.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      symbol.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || symbol.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const sortedSymbols = [...filteredSymbols].sort((a, b) => {
    switch (sortBy) {
      case 'name':
        return a.name.localeCompare(b.name);
      case 'progress':
        return b.progress - a.progress;
      case 'recent':
        // This assumes we have a lastInteraction field, which we might want to add
        return 0;
      default:
        return 0;
    }
  });

  const handleInteraction = (symbol: Symbol, type: 'study' | 'meditation' | 'practice' | 'insight') => {
    onSymbolInteraction(symbol.id, type);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search symbols..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex gap-2">
          <Select
            value={selectedCategory}
            onValueChange={(value) => setSelectedCategory(value as SymbolCategory | 'all')}
          >
            <SelectTrigger className="w-[180px]">
              <Filter className="w-4 h-4 mr-2" />
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              {CATEGORIES.map((category) => (
                <SelectItem key={category} value={category}>
                  {category.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Select
            value={sortBy}
            onValueChange={(value) => setSortBy(value as 'name' | 'progress' | 'recent')}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="name">Name</SelectItem>
              <SelectItem value="progress">Progress</SelectItem>
              <SelectItem value="recent">Recent</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {sortedSymbols.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-lg text-muted-foreground mb-4">
            No symbols found matching your criteria
          </p>
          <Button variant="outline" onClick={() => {
            setSearchQuery('');
            setSelectedCategory('all');
          }}>
            Clear Filters
          </Button>
        </div>
      ) : (
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
        >
          {sortedSymbols.map((symbol) => (
            <motion.div key={symbol.id} variants={item}>
              <SymbolCard
                symbol={symbol}
                onInteract={(type) => handleInteraction(symbol, type)}
              />
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}