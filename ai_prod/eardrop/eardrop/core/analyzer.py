"""
Audio differentiation analysis module
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy.spatial.distance import cosine, euclidean, cityblock
from scipy.stats import pearsonr

from ..config import Config, AnalyzerConfig
from .feature_extractor import FeatureExtractor


class Analyzer:
    """Analyze differences between audio features"""
    
    def __init__(self, config: Optional[AnalyzerConfig] = None):
        """
        Initialize Analyzer
        
        Args:
            config: AnalyzerConfig instance
        """
        self.config = config or Config.analyzer
        self.feature_extractor = FeatureExtractor()
    
    def compare(self, features1: Dict[str, np.ndarray], 
                features2: Dict[str, np.ndarray]) -> Dict[str, float]:
        """
        Compare two feature sets and compute similarity/difference metrics
        
        Args:
            features1: First feature dictionary
            features2: Second feature dictionary
            
        Returns:
            Dictionary of comparison metrics
        """
        # Get feature vectors for comparison
        vec1 = self.feature_extractor.get_feature_vector(features1)
        vec2 = self.feature_extractor.get_feature_vector(features2)
        
        # Normalize if configured
        if self.config.normalize_features:
            vec1 = self._normalize(vec1)
            vec2 = self._normalize(vec2)
        
        # Compute similarity metrics
        results = {}
        
        # Cosine similarity
        if self.config.similarity_metric == 'cosine':
            similarity = 1 - cosine(vec1, vec2)
            distance = cosine(vec1, vec2)
        elif self.config.similarity_metric == 'euclidean':
            distance = euclidean(vec1, vec2)
            similarity = 1 / (1 + distance)  # Convert to similarity
        elif self.config.similarity_metric == 'manhattan':
            distance = cityblock(vec1, vec2)
            similarity = 1 / (1 + distance)  # Convert to similarity
        else:
            raise ValueError(f"Unknown similarity metric: {self.config.similarity_metric}")
        
        results['similarity'] = float(similarity)
        results['distance'] = float(distance)
        
        # Pearson correlation
        if len(vec1) == len(vec2) and len(vec1) > 1:
            correlation, p_value = pearsonr(vec1, vec2)
            results['correlation'] = float(correlation)
            results['correlation_p_value'] = float(p_value)
        
        # Per-feature comparison
        feature_comparisons = self._compare_features(features1, features2)
        results['feature_comparisons'] = feature_comparisons
        
        # Overall difference score (0 = identical, 1 = completely different)
        results['difference_score'] = 1 - similarity
        
        return results
    
    def _compare_features(self, features1: Dict[str, np.ndarray],
                         features2: Dict[str, np.ndarray]) -> Dict[str, Dict[str, float]]:
        """
        Compare individual features
        
        Args:
            features1: First feature dictionary
            features2: Second feature dictionary
            
        Returns:
            Dictionary of per-feature comparisons
        """
        comparisons = {}
        
        # Get common features
        common_features = set(features1.keys()) & set(features2.keys())
        
        for feature_name in common_features:
            feat1 = features1[feature_name]
            feat2 = features2[feature_name]
            
            # Handle different shapes
            if feat1.shape != feat2.shape:
                # Try to align by taking minimum length
                min_len = min(feat1.shape[-1], feat2.shape[-1])
                if feat1.ndim == 1:
                    feat1 = feat1[:min_len]
                    feat2 = feat2[:min_len]
                else:
                    feat1 = feat1[:, :min_len]
                    feat2 = feat2[:, :min_len]
            
            # Compute statistics
            if feat1.ndim == 1:
                diff = np.abs(feat1 - feat2)
                comparisons[feature_name] = {
                    'mean_difference': float(np.mean(diff)),
                    'max_difference': float(np.max(diff)),
                    'std_difference': float(np.std(diff)),
                    'relative_difference': float(np.mean(diff) / (np.mean(np.abs(feat1)) + 1e-10))
                }
            else:
                # For 2D features, compute per-dimension then aggregate
                dim_diffs = []
                for dim in range(min(feat1.shape[0], feat2.shape[0])):
                    dim_diff = np.abs(feat1[dim, :] - feat2[dim, :])
                    dim_diffs.append(dim_diff)
                
                all_diffs = np.concatenate(dim_diffs)
                comparisons[feature_name] = {
                    'mean_difference': float(np.mean(all_diffs)),
                    'max_difference': float(np.max(all_diffs)),
                    'std_difference': float(np.std(all_diffs)),
                    'relative_difference': float(np.mean(all_diffs) / (np.mean(np.abs(feat1)) + 1e-10))
                }
        
        return comparisons
    
    def batch_compare(self, feature_list: List[Dict[str, np.ndarray]]) -> np.ndarray:
        """
        Compare multiple feature sets pairwise
        
        Args:
            feature_list: List of feature dictionaries
            
        Returns:
            Similarity matrix (n x n)
        """
        n = len(feature_list)
        similarity_matrix = np.zeros((n, n))
        
        # Extract feature vectors
        vectors = []
        for features in feature_list:
            vec = self.feature_extractor.get_feature_vector(features)
            if self.config.normalize_features:
                vec = self._normalize(vec)
            vectors.append(vec)
        
        # Compute pairwise similarities
        for i in range(n):
            for j in range(n):
                if i == j:
                    similarity_matrix[i, j] = 1.0
                else:
                    if self.config.similarity_metric == 'cosine':
                        sim = 1 - cosine(vectors[i], vectors[j])
                    elif self.config.similarity_metric == 'euclidean':
                        dist = euclidean(vectors[i], vectors[j])
                        sim = 1 / (1 + dist)
                    elif self.config.similarity_metric == 'manhattan':
                        dist = cityblock(vectors[i], vectors[j])
                        sim = 1 / (1 + dist)
                    else:
                        raise ValueError(f"Unknown similarity metric: {self.config.similarity_metric}")
                    
                    similarity_matrix[i, j] = sim
        
        return similarity_matrix
    
    def find_most_similar(self, target_features: Dict[str, np.ndarray],
                         candidate_features: List[Dict[str, np.ndarray]],
                         top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Find most similar features from a list of candidates
        
        Args:
            target_features: Target feature dictionary
            candidate_features: List of candidate feature dictionaries
            top_k: Number of top results to return
            
        Returns:
            List of (index, similarity) tuples, sorted by similarity (descending)
        """
        similarities = []
        
        target_vec = self.feature_extractor.get_feature_vector(target_features)
        if self.config.normalize_features:
            target_vec = self._normalize(target_vec)
        
        for idx, candidate in enumerate(candidate_features):
            candidate_vec = self.feature_extractor.get_feature_vector(candidate)
            if self.config.normalize_features:
                candidate_vec = self._normalize(candidate_vec)
            
            if self.config.similarity_metric == 'cosine':
                sim = 1 - cosine(target_vec, candidate_vec)
            elif self.config.similarity_metric == 'euclidean':
                dist = euclidean(target_vec, candidate_vec)
                sim = 1 / (1 + dist)
            elif self.config.similarity_metric == 'manhattan':
                dist = cityblock(target_vec, candidate_vec)
                sim = 1 / (1 + dist)
            else:
                raise ValueError(f"Unknown similarity metric: {self.config.similarity_metric}")
            
            similarities.append((idx, sim))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        """
        Normalize feature vector
        
        Args:
            vector: Feature vector
            
        Returns:
            Normalized feature vector
        """
        norm = np.linalg.norm(vector)
        if norm > 0:
            return vector / norm
        return vector
    
    def get_difference_report(self, features1: Dict[str, np.ndarray],
                             features2: Dict[str, np.ndarray]) -> str:
        """
        Generate a human-readable difference report
        
        Args:
            features1: First feature dictionary
            features2: Second feature dictionary
            
        Returns:
            Formatted report string
        """
        comparison = self.compare(features1, features2)
        
        report = []
        report.append("=" * 60)
        report.append("Audio Feature Comparison Report")
        report.append("=" * 60)
        report.append(f"\nOverall Similarity: {comparison['similarity']:.4f}")
        report.append(f"Overall Distance: {comparison['distance']:.4f}")
        report.append(f"Difference Score: {comparison['difference_score']:.4f}")
        
        if 'correlation' in comparison:
            report.append(f"Pearson Correlation: {comparison['correlation']:.4f}")
            report.append(f"Correlation P-value: {comparison['correlation_p_value']:.4f}")
        
        report.append("\n" + "-" * 60)
        report.append("Per-Feature Differences:")
        report.append("-" * 60)
        
        for feature_name, feat_comp in comparison['feature_comparisons'].items():
            report.append(f"\n{feature_name}:")
            report.append(f"  Mean Difference: {feat_comp['mean_difference']:.4f}")
            report.append(f"  Max Difference: {feat_comp['max_difference']:.4f}")
            report.append(f"  Relative Difference: {feat_comp['relative_difference']:.4f}")
        
        return "\n".join(report)
