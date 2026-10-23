export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

export type ExecutionStatus =
  | 'Draft'
  | 'Validating'
  | 'Ready'
  | 'Running (Simulator)'
  | 'Running (Hardware)'
  | 'Complete'
  | 'Failed'
  | 'Cancelled';

export interface ExplanationByLevel {
  beginner: string;
  intermediate: string;
  technical: string;
}

export interface Template {
  template_id: string;
  name: string;
  description: string;
  difficulty: DifficultyLevel;
  category: string;
  prompt_text: string;
  suggestion_chips: string[];
  qiskit_code: string;
  circuit_description: string;
  explanation_by_level: ExplanationByLevel;
}

export interface ValidationReport {
  is_valid: boolean;
  syntax_passed: boolean;
  imports_passed: boolean;
  safety_passed: boolean;
  circuit_valid: boolean;
  errors: string[];
  unauthorized_imports: string[];
  blocked_keywords: string[];
}

export interface ExecutionConfig {
  primitive_type: 'Sampler' | 'Estimator';
  backend_id: string;
  shots: number;
  mode: string;
  transpiler_settings: {
    optimization_level: number;
    coupling_map?: number[][];
    basis_gates?: string[];
  };
}

export interface ExecutionResult {
  raw_result?: Record<string, number>;
  backend_metadata: Record<string, any>;
  status: ExecutionStatus;
  error_message?: string;
  execution_time_ms?: number;
  timestamps: Record<string, string>;
}

export interface SharingState {
  private: boolean;
  repository: boolean;
  dataset: boolean;
  social: boolean;
  research_package: boolean;
  consent_timestamps: Record<string, string>;
}

export interface Provenance {
  qiskit_version: string;
  qiskit_aer_version: string;
  adapter_used: string;
  schema_version: string;
  hardware_confirmed: boolean;
}

export interface ExperimentRecord {
  experiment_id: string;
  owner_id: string;
  created_at: string;
  updated_at: string;
  prompt_text: string;
  template_id?: string;
  generated_code: string;
  user_edited_code?: string;
  code_version_history: Array<{
    version: number;
    code: string;
    author: 'ai' | 'user';
    timestamp: string;
  }>;
  circuit_description?: string;
  validation_report?: ValidationReport;
  execution_config: ExecutionConfig;
  execution_result: ExecutionResult;
  explanation_by_level?: ExplanationByLevel;
  sharing_state: SharingState;
  provenance: Provenance;
}

export interface ProviderInfo {
  id: string;
  name: string;
  type: 'simulator' | 'hardware';
  status: string;
  description: string;
  requires_confirmation: boolean;
}
