import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ImageIcon } from "lucide-react";

interface Product {
  uniq_id: string;
  title: string;
  price: number;
  brand: string;
  images?: string;
  creative_description: string;
  similarity_score: number;
}

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <Card 
      className="overflow-hidden hover-elevate transition-all duration-200 hover:scale-[1.02] flex flex-col"
      data-testid={`card-product-${product.uniq_id}`}
    >
      <CardHeader className="p-0">
        <div className="aspect-[4/3] bg-muted relative overflow-hidden">
          {product.images ? (
            <img
              src={product.images}
              alt={product.title}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
                e.currentTarget.nextElementSibling?.classList.remove('hidden');
              }}
              data-testid={`img-product-${product.uniq_id}`}
            />
          ) : null}
          <div className="hidden absolute inset-0 flex items-center justify-center bg-muted">
            <ImageIcon className="w-12 h-12 text-muted-foreground/30" />
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="p-4 flex-1 flex flex-col gap-2">
        <div className="flex items-start justify-between gap-2">
          <h3 
            className="font-medium text-base line-clamp-2 leading-tight flex-1"
            data-testid={`text-title-${product.uniq_id}`}
          >
            {product.title}
          </h3>
        </div>
        
        <div className="flex items-center gap-2">
          <Badge variant="secondary" className="text-xs">
            {product.brand}
          </Badge>
          <span 
            className="text-lg font-semibold text-primary ml-auto"
            data-testid={`text-price-${product.uniq_id}`}
          >
            ${product.price.toFixed(2)}
          </span>
        </div>
        
        <p 
          className="text-sm text-muted-foreground line-clamp-3 italic leading-relaxed mt-1"
          data-testid={`text-description-${product.uniq_id}`}
        >
          {product.creative_description}
        </p>
      </CardContent>
      
      <CardFooter className="p-4 pt-0">
        <div className="w-full flex items-center justify-between text-xs text-muted-foreground">
          <span>Match: {(product.similarity_score * 100).toFixed(0)}%</span>
        </div>
      </CardFooter>
    </Card>
  );
}
