import { useState } from 'react'
import { Search, ArrowLeft, Loader2, ExternalLink } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { searchApi, type SearchResult } from '@/lib/api'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [sourceFilter, setSourceFilter] = useState<string>()

  const handleSearch = async () => {
    if (!query.trim()) return

    setIsLoading(true)
    setHasSearched(true)

    try {
      const response = await searchApi.search(query, sourceFilter, 20)
      setResults(response.results)
    } catch (error) {
      console.error('Search error:', error)
      setResults([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <Link to="/">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour au chat
            </Button>
          </Link>
        </div>
      </header>

      {/* Search Section */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">Recherche dans la base</h1>
          <p className="text-gray-600">
            Recherchez dans les bases Vidal et Meddispar
          </p>
        </div>

        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex gap-2 mb-4">
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Rechercher un médicament, une maladie..."
                className="flex-1"
              />
              <Button onClick={handleSearch} disabled={isLoading || !query.trim()}>
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                ) : (
                  <Search className="w-4 h-4 mr-2" />
                )}
                Rechercher
              </Button>
            </div>

            <div className="flex gap-2">
              <Button
                variant={sourceFilter === undefined ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSourceFilter(undefined)}
              >
                Toutes les sources
              </Button>
              <Button
                variant={sourceFilter === 'vidal' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSourceFilter('vidal')}
              >
                Vidal
              </Button>
              <Button
                variant={sourceFilter === 'meddispar' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSourceFilter('meddispar')}
              >
                Meddispar
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        {isLoading ? (
          <div className="text-center py-12">
            <Loader2 className="w-8 h-8 animate-spin mx-auto text-primary mb-4" />
            <p className="text-gray-600">Recherche en cours...</p>
          </div>
        ) : hasSearched ? (
          results.length > 0 ? (
            <div className="space-y-4">
              <p className="text-sm text-gray-600">
                {results.length} résultat{results.length > 1 ? 's' : ''} trouvé
                {results.length > 1 ? 's' : ''}
              </p>
              {results.map((result, index) => (
                <Card key={index} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between gap-4">
                      <CardTitle className="text-lg">{result.title}</CardTitle>
                      <Badge
                        variant={
                          result.source_type === 'vidal' ? 'default' : 'secondary'
                        }
                      >
                        {result.source_type}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-700 mb-3">{result.content}</p>
                    {result.url && (
                      <a
                        href={result.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm text-primary hover:underline"
                      >
                        Voir la source
                        <ExternalLink className="w-3 h-3 ml-1" />
                      </a>
                    )}
                    <div className="mt-2">
                      <span className="text-xs text-gray-500">
                        Pertinence: {(result.relevance_score * 100).toFixed(0)}%
                      </span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="text-center py-12">
              <CardContent>
                <p className="text-gray-600 mb-2">Aucun résultat trouvé</p>
                <p className="text-sm text-gray-500">
                  Essayez avec d'autres mots-clés
                </p>
              </CardContent>
            </Card>
          )
        ) : null}
      </div>
    </div>
  )
}
